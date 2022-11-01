from rest_framework import serializers

from .models.main_models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = '__all__'
