from rest_framework import serializers

from .models import KumbioUser

class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = KumbioUser
        exclude = ('password',)


class CreateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = KumbioUser
        fields = ( "id", "email", "username", "password", "organization", "first_name", "last_name")