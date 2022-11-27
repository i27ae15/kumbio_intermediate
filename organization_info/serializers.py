from rest_framework import serializers

from .models.main_models import (Organization, OrganizationProfessional, OrganizationPlace, OrganizationService, Sector, DayAvailableForPlace, OrganizationClient)
from user_info.serializers import KumbioUserSerializer


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


class OrganizationClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationClient
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'deleted_by', 'updated_by', 'referral_link')