from rest_framework import serializers

from .models.main_models import Organization, OrganizationProfessional
from user_info.serializers import KumbioUserSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = '__all__'

# change this to nested serializers to exclude fields
class OrganizationProfessionalSerializer(serializers.ModelSerializer):
    
    created_by_id = serializers.IntegerField(write_only=True)
    kumbio_user_id = serializers.IntegerField(write_only=True)
    organization_id = serializers.CharField(write_only=True)
    
    # kumbio_user = KumbioUserSerializer(read_only=True)
    
    class Meta:
        model = OrganizationProfessional
        fields = '__all__'
        # exclude = ('kumbio_user', 'created_by', 'organization')
        # write_only_fields = ('created_by', 'organization', 'created_by_id', 'organization_id')
        depth = 1