from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import AppointmentInvoice
from organization_info.models.main_models import Organization, PaymentMethodAcceptedByOrg

from print_pp.logging import Print

class AppointmentInvoiceSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        organization:Organization = attrs['organization']
        try: organization.payment_methods_accepted.get(id=attrs['payment_method'].pk)
        except PaymentMethodAcceptedByOrg.DoesNotExist: raise serializers.ValidationError(_("El método de pago no existe o no es aceptado por la organización"))
        
        return super().validate(attrs)

    class Meta:
        model = AppointmentInvoice
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'updated_by', 'deleted_by')