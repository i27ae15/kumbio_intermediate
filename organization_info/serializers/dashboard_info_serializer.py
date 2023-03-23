from rest_framework import serializers
from organization_info.models.main_models import Organization, OrganizationPlace, OrganizationService
from .model_serializers import (DayAvailableForPlaceSerializer, DayAvailableForProfessionalSerializer, 
OrganizationProfessionalSerializer, OrganizationServiceSerializer, OrganizationProfessional, OrganizationPlaceSerializer)

class OrganizationDashboardInfoSerializer(serializers.ModelSerializer):

    
    organizationplace_set = OrganizationPlaceSerializer(many=True, read_only=True)
    organization_professionals = OrganizationProfessionalSerializer(many=True, read_only=True)


    organizationservice_set = serializers.SerializerMethodField()

    def get_organizationservice_set(self, instance:Organization):
        services = instance.organizationservice_set.filter(deleted_at__isnull=True)
        return OrganizationServiceSerializer(services, many=True).data


    class Meta:
        model = Organization
        fields = [ 'id', 'name', 'logo', 'country', 'description', 'organizationservice_set', 'organizationplace_set', 'organization_professionals', 'about_us_image', 'banner_text', 'banner_image', 'slogan', 'language']
        read_only_fields = [ 'id', 'name', 'logo', 'country', 'description', 'organizationservice_set', 'organizationplace_set', 'organization_professionals', 'about_us_image', 'banner_text', 'banner_image', 'slogan', 'language']


class OrganizationServiceDashboardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationService
        fields = ['id', 'service', 'price', 'time_interval', 'description']
        read_only_fields = ['id', 'service', 'price', 'time_interval', 'description']


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