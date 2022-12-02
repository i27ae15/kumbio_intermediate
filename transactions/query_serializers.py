from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from organization_info.models.main_models import Organization, PaymentMethodAcceptedByOrg

from .models import AppointmentInvoice


class AppointmentInvoiceQuerySerializer(serializers.Serializer):

    appointment_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id de la cita que se quiere obtener")
    invoice_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id de la factura que se quiere obtener")

    min_amount = serializers.IntegerField(default=0, help_text="Monto mínimo de la factura que se quiere obtener")
    max_amount = serializers.IntegerField(default=float('inf'), help_text="Monto máximo de la factura que se quiere obtener")

    status = serializers.CharField(default=None, allow_null=True, help_text="Estado de la factura que se quiere obtener")

    from_date = serializers.DateField(default=None, allow_null=True, help_text="Fecha de inicio de la factura que se quiere obtener")
    to_date = serializers.DateField(default=None, allow_null=True, help_text="Fecha de fin de la factura que se quiere obtener")

    services = serializers.ListField(default=None, allow_null=True, help_text="Lista de servicios que se quiere obtener")
    products = serializers.ListField(default=None, allow_null=True, help_text="Lista de productos que se quiere obtener")

    payment_method = serializers.IntegerField(default=None, allow_null=True, help_text="Método de pago de la factura que se quiere obtener")


    def validate(self, attrs):

        if not attrs['appointment_id'] and not attrs['invoice_id']:
            # this will mean that the user is trying to get all the invoices of its organization
            organization_id:int = self.context['organization_id']
            
            try: organization:Organization = Organization.objects.get(id=organization_id)
            except Organization.DoesNotExist: raise serializers.ValidationError(_("La organización no existe"))
            attrs['organization'] = organization
            
            try: payment_method:PaymentMethodAcceptedByOrg = organization.payment_methods_accepted.get(id=attrs['payment_method'])
            except PaymentMethodAcceptedByOrg.DoesNotExist: raise serializers.ValidationError(_("El método de pago no existe o no es aceptado por la organización"))
            attrs['payment_method'] = payment_method
            
        elif attrs['appointment_id']:
            # this will mean that the user is trying to get the invoice of a specific appointment
            # so we need to make a call to the calendar_api to check if the appointment exists
            pass

        elif attrs['invoice_id']:
            # this will mean that the user is trying to get a specific invoice
            try: invoice:AppointmentInvoice = AppointmentInvoice.objects.get(id=attrs['invoice_id'])
            except AppointmentInvoice.DoesNotExist: raise serializers.ValidationError(_("La factura no existe"))
            attrs['invoice'] = invoice

        return super().validate(attrs)