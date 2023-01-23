from rest_framework import serializers
from organization_info.models.main_models import Organization, OrganizationPlace, OrganizationService
from .model_serializers import (DayAvailableForPlaceSerializer, DayAvailableForProfessionalSerializer, 
OrganizationProfessionalSerializer, OrganizationServiceSerializer, OrganizationProfessional, OrganizationPlaceSerializer)

class OrganizationDashboardInfoSerializer(serializers.ModelSerializer):

    organizationservice_set = OrganizationServiceSerializer(many=True, read_only=True)
    organizationplace_set = OrganizationPlaceSerializer(many=True, read_only=True)
    organization_professionals = OrganizationProfessionalSerializer(many=True, read_only=True)


    class Meta:
        model = Organization
        fields = [ 'id', 'name', 'logo', 'country', 'description', 'organizationservice_set', 'organizationplace_set', 'organization_professionals']
        read_only_fields = [ 'id', 'name', 'logo', 'country', 'description', 'organizationservice_set', 'organizationplace_set', 'organization_professionals']


class OrganizationServiceDashboardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationService
        fields = ['id', 'service', 'price', 'time_interval', 'description',]
        read_only_fields = ['id', 'service', 'price', 'time_interval', 'description',]


class OrganizationProfessionalDashboardInfoSerializer(serializers.ModelSerializer):

    dayavailableforprofessional_set = DayAvailableForProfessionalSerializer(many=True, read_only=True)

    class Meta:
        model = OrganizationProfessional
        fields = ['id', 'profile_photo', 'academic_formation', 'about_me', 'dayavailableforprofessional_set']
        read_only_fields = ['id', 'profile_photo', 'academic_formation', 'about_me', 'dayavailableforprofessional_set']
        depth = 1


class OrganizationPlaceDashboardInfoSerializer(serializers.ModelSerializer):

    dayavailableforplace_set = DayAvailableForPlaceSerializer(many=True, read_only=True)

    class Meta:
        model = OrganizationPlace
        fields = ['id', 'name', 'address', 'dayavailableforplace_set']
        read_only_fields = ['id', 'name', 'address', 'dayavailableforplace_set']