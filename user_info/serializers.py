from rest_framework import serializers

from .models import KumbioUser, NotificationsSettings

from print_pp.logging import Print, check_caller_line


class NotificationsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsSettings
        fields = '__all__'

class KumbioUserSerializer(serializers.ModelSerializer):    
    
    notificationssettings_set = NotificationsSettingsSerializer(many=True)
    
    class Meta:
        model = KumbioUser
        exclude = ('password', 'extra_permissions')
        read_only_fields = ('calendar_token', 'selene_token')


class CreateKumbioUserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        
        set_verified_email = self.context.get('set_verified_email')
            
        user = KumbioUser(**validated_data)
        user.save(set_verified_email=set_verified_email)
        
        return user

    
    class Meta:
        model = KumbioUser
        fields = ( "id", "email", "username", "password", "organization", "first_name", "last_name")


class KumbioUserAvailablePlacesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = KumbioUser
        fields = ("available_places",)
        depth = 1
        
        
class KumbioUserAvailableServicesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = KumbioUser
        fields = ("available_services",)
        depth = 1