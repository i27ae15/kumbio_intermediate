from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models.main_models import (Organization, OrganizationProfessional, OrganizationPlace, 
OrganizationService, Sector, DayAvailableForPlace, OrganizationClient, ClientParent,
OrganizationClientType, DayAvailableForProfessional)
from ..utils.enums import FieldType

from print_pp.logging import Print

from utils.time import change_exclusion_timezone


def organization_class_serializer():
    return OrganizationClientSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = '__all__'


class DayAvailableForProfessionalExcludeInLocalSerializer(serializers.ModelSerializer):

    exclude = serializers.SerializerMethodField()
    exclusion = serializers.SerializerMethodField()


    def get_exclude(self, instance: DayAvailableForProfessional):
        return change_exclusion_timezone(instance.exclude, 'UTC', instance.professional.organization.default_timezone)

    
    def get_exclusion(self, instance: DayAvailableForProfessional):
        return change_exclusion_timezone(instance.exclusion, 'UTC', instance.professional.organization.default_timezone)

    class Meta:
        model = DayAvailableForProfessional
        fields = '__all__'



class DayAvailableForProfessionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayAvailableForProfessional
        fields = '__all__'


# change this to nested serializers to exclude fields
# look for the bug that does not let us use nested serializers  
class OrganizationProfessionalSerializer(serializers.ModelSerializer):
    
    created_by_id = serializers.IntegerField(write_only=True, required=False)
    kumbio_user_id = serializers.IntegerField(write_only=True, required=False)
    organization_id = serializers.CharField(write_only=True, required=False)
    place_id = serializers.IntegerField(write_only=True, required=False)
    services_ids = serializers.ListField(write_only=True, required=False)
    specialties_ids = serializers.ListField(write_only=True, required=False)

    dayavailableforprofessional_set = DayAvailableForProfessionalExcludeInLocalSerializer(many=True, read_only=True)

    class Meta:
        model = OrganizationProfessional
        fields = '__all__'
        depth = 1


class DayAvailableForPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayAvailableForPlace
        fields = '__all__'


class OrganizationPlaceSerializer(serializers.ModelSerializer):

    dayavailableforplace_set = DayAvailableForPlaceSerializer(many=True, read_only=True)


    class Meta:
        model = OrganizationPlace
        fields = '__all__'


class OrganizationServiceSerializer(serializers.ModelSerializer):

    organizationprofessional_set = OrganizationProfessionalSerializer(many=True, read_only=True)

    class Meta:
        model = OrganizationService
        fields = '__all__'


class OrganizationSectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = '__all__'


class OrganizationClientTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationClientType
        exclude = ('deleted_by', 'deleted_at', 'organization')


class OrganizationClientSerializer(serializers.ModelSerializer):
    
    def validate(self, data):

        extra_fields = data.get('extra_fields', None)
        if not extra_fields:
            raise serializers.ValidationError(_('Extra fields are required'))

        for field in extra_fields:
            if len(field) != 3:
                raise serializers.ValidationError(_('extra_fields Debe tener 3 elementos: nombre, tipo, valor. Ejemplo: ["pets_first_name", TEXT, "Ricardo"]'))
            
            if field[1] not in [FieldType.TEXT.value, FieldType.NUMBER.value]:
                raise serializers.ValidationError(_('Tipo de campo no válido. Debe ser TEXT o NUMBER'))

            if field[1] == FieldType.NUMBER.value:
                try:
                    int(field[2])
                except ValueError:
                    raise serializers.ValidationError(_('Valor de campo no válido. Debe ser un número'))
            
            if field[1] == FieldType.TEXT.value:
                if not isinstance(field[2], str):
                    raise serializers.ValidationError(_('Valor de campo no válido. Debe ser texto'))
            
            if not isinstance(field[0], str):
                raise serializers.ValidationError(_('Nombre de campo no válido. Debe ser texto'))

            field = tuple(field)

        return data


    class Meta:
        model = OrganizationClient
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'deleted_by', 'updated_by', 'referral_link')



class ClientParentSerializer(serializers.ModelSerializer):


    class Meta:
        model = ClientParent
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class OrganizationClientRelatedFieldsSerializer(serializers.ModelSerializer):

    type = OrganizationClientTypeSerializer()
    
    # TODO: Change this to a serializer
    client_parent = serializers.SerializerMethodField()

    def get_client_parent(self, obj:OrganizationClient):
        return {
            'id': obj.client_parent.pk,
            'first_name': obj.client_parent.first_name,
            'last_name': obj.client_parent.last_name,
            'email': obj.client_parent.email,
            'phone': obj.client_parent.phone,
        }
    
    
    class Meta:
        model = OrganizationClient
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'deleted_by', 'updated_by', 'referral_link')



