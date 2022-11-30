from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


from .models.main_models import (Organization, OrganizationProfessional, OrganizationPlace, 
OrganizationService, Sector, DayAvailableForPlace, OrganizationClient, OrganizationClientDependent,
OrganizationClientType)
from user_info.serializers import KumbioUserSerializer
from .utils.enums import FieldType


class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = '__all__'


# change this to nested serializers to exclude fields
# look for the bug that does not let us use nested serializers
class OrganizationProfessionalSerializer(serializers.ModelSerializer):
    
    created_by_id = serializers.IntegerField(write_only=True)
    kumbio_user_id = serializers.IntegerField(write_only=True)
    organization_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = OrganizationProfessional
        fields = '__all__'
        depth = 1


class OrganizationPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationPlace
        fields = '__all__'


class OrganizationServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationService
        fields = '__all__'


class OrganizationSectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = '__all__'


class DayAvailableForPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayAvailableForPlace
        fields = '__all__'


class OrganizationClientDependentFromSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationClientDependent
        fields = '__all__'


class OrganizationClientTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationClientType
        exclude = ('deleted_by', 'deleted_at', 'organization')


class OrganizationClientSerializer(serializers.ModelSerializer):

    client_dependent = OrganizationClientDependentFromSerializer(many=True, read_only=True)
    client_type = OrganizationClientTypeSerializer(many=True, read_only=True)

    def validate(self, data):

        extra_fields = data.get('extra_fields', None)
        if not extra_fields:
            raise serializers.ValidationError('Extra fields are required')

        for field in extra_fields:
            if len(field) != 3:
                raise serializers.ValidationError('extra_fields Debe tener 3 elementos: nombre, tipo, valor. Ejemplo: ["pets_first_name", TEXT, "Ricardo"]')
            
            if field[1] not in [FieldType.TEXT.value, FieldType.NUMBER.value]:
                raise serializers.ValidationError('Tipo de campo no válido. Debe ser TEXT o NUMBER')

            if field[1] == FieldType.NUMBER.value:
                try:
                    int(field[2])
                except ValueError:
                    raise serializers.ValidationError('Valor de campo no válido. Debe ser un número')
            
            if field[1] == FieldType.TEXT.value:
                if not isinstance(field[2], str):
                    raise serializers.ValidationError('Valor de campo no válido. Debe ser texto')
            
            if not isinstance(field[0], str):
                raise serializers.ValidationError('Nombre de campo no válido. Debe ser texto')

            field = tuple(field)

        return data

    class Meta:
        model = OrganizationClient
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'deleted_by', 'updated_by', 'referral_link')

