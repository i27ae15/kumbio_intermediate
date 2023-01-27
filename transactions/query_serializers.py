# import datetime

# from django.utils.translation import gettext_lazy as _

# from rest_framework import serializers

# from organization_info.models.main_models import Organization, PaymentMethodAcceptedByOrg, OrganizationClient

# from .models import AppointmentInvoice


# class AppointmentInvoiceQuerySerializer(serializers.Serializer):

#     appointment_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id de la cita que se quiere obtener")
#     invoice_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id de la factura que se quiere obtener")
#     client_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id del cliente que se quiere obtener")

#     min_amount = serializers.IntegerField(default=0, help_text="Monto mínimo de la factura que se quiere obtener")
#     max_amount = serializers.IntegerField(default=float('inf'), help_text="Monto máximo de la factura que se quiere obtener")

#     status = serializers.CharField(default=None, allow_null=True, help_text="Estado de la factura que se quiere obtener")

#     from_date = serializers.DateField(default=None, allow_null=True, help_text="Fecha de inicio de la factura que se quiere obtener")
#     to_date = serializers.DateField(default=None, allow_null=True, help_text="Fecha de fin de la factura que se quiere obtener")

#     services = serializers.ListField(default=None, allow_null=True, help_text="Lista de servicios que se quiere obtener")
#     products = serializers.ListField(default=None, allow_null=True, help_text="Lista de productos que se quiere obtener")

#     payment_method = serializers.IntegerField(default=None, allow_null=True, help_text="Método de pago de la factura que se quiere obtener")


#     def validate(self, attrs:dict):

#         if not attrs['appointment_id'] and not attrs['invoice_id'] and not attrs['client_id']:
#             self.convert_and_delete_serializer_attributes(attrs)

#         elif attrs['appointment_id']:
#             # this will mean that the user is trying to get the invoice of a specific appointment
#             # so we need to make a call to the calendar_api to check if the appointment exists
#             pass

#         elif attrs['invoice_id']:
#             # this will mean that the user is trying to get a specific invoice
#             try: invoice:AppointmentInvoice = AppointmentInvoice.objects.get(id=attrs['invoice_id'])
#             except AppointmentInvoice.DoesNotExist: raise serializers.ValidationError(_("La factura no existe"))
#             attrs['invoice'] = invoice
        
#         elif attrs['client_id']:
#             # this will mean that the user is trying to get all the invoices of a specific client
#             try: client:OrganizationClient = OrganizationClient.objects.get(id=attrs['client_id'])
#             except OrganizationClient.DoesNotExist: raise serializers.ValidationError(_("El cliente no existe"))
#             attrs['client'] = client    

#         return super().validate(attrs)


#     def convert_and_delete_serializer_attributes(self, attrs:dict) -> None:

#         # delete the keywords that are marked as None so that
#         # they don't get passed to the queryset filter


#         del attrs['appointment_id']
#         del attrs['invoice_id']
#         del attrs['client_id']

#         # this will mean that the user is trying to get all the invoices of its organization
#         organization_id:int = self.context['organization_id']
        
#         try: organization:Organization = Organization.objects.get(id=organization_id)
#         except Organization.DoesNotExist: raise serializers.ValidationError(_("La organización no existe"))
#         attrs['organization'] = organization.pk
        
#         if attrs.get('payment_method'):
#             try: payment_method:PaymentMethodAcceptedByOrg = organization.payment_methods_accepted.get(id=attrs['payment_method'])
#             except PaymentMethodAcceptedByOrg.DoesNotExist: raise serializers.ValidationError(_("El método de pago no existe o no es aceptado por la organización"))
#             attrs['payment_method'] = payment_method.pk
#         else:
#             del attrs['payment_method']
        
#         if not attrs.get('status'): del attrs['status']
#         if not attrs.get('from_date'): del attrs['from_date']
#         if not attrs.get('to_date'): del attrs['to_date']
#         if not attrs.get('services'): del attrs['services']
#         if not attrs.get('products'): del attrs['products']

#         attrs['amount__gte'] = attrs['min_amount']
#         attrs['amount__lte'] = attrs['max_amount']

#         del attrs['min_amount']
#         del attrs['max_amount']

#         # convert the date to datetime
#         if attrs.get('from_date'): attrs['created_at__gte'] = datetime.datetime.combine(attrs['from_date'], datetime.datetime.min.time()); del attrs['from_date']
#         if attrs.get('to_date'): attrs['created_at__lte'] = datetime.datetime.combine(attrs['to_date'], datetime.datetime.max.time()); del attrs['to_date']
