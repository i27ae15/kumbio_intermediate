from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from user_info.models import KumbioUser, NotificationsSettings

from print_pp.logging import Print


class ChangePasswordBodySerializer(serializers.Serializer):
    code:str = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)

    def validate(self, attrs):
        
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise exceptions.ValidationError(_('Las contraseñas no coinciden'))

        self.__convert_to_objects(attrs)

        user:KumbioUser = attrs['user']
        if user.code_to_recover_password_date_expiration < timezone.now():
            raise exceptions.ValidationError(_('El código ha expirado'))
            
        return super().validate(attrs)
    

    def __convert_to_objects(self, attrs:dict):
        try: attrs['user'] = KumbioUser.objects.get(code_to_recover_password=attrs['code'])
        except KumbioUser.DoesNotExist: 
            raise exceptions.NotFound(_('El usuario no existe'))


class RecoverPasswordBodySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)
    

    def __convert_to_objects(self, attrs:dict):
        try: attrs['user'] = KumbioUser.objects.get(email=attrs['email'])
        except KumbioUser.DoesNotExist: 
            return exceptions.NotFound(_('El usuario no existe'))


class TaskBodySerializer(serializers.Serializer):

    task = serializers.CharField(required=True)


class TaskToUpdateBodySerializer(serializers.Serializer):

    task_id = serializers.IntegerField(required=True)
    task = serializers.CharField(required=True)


class TaskToDeleteBodySerializer(serializers.Serializer):

    task_id = serializers.IntegerField(required=True)
