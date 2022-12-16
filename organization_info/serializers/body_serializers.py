from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from .model_serializers import OrganizationClientSerializer, OrganizationProfessionalSerializer
from organization_info.models.main_models import OrganizationProfessional

class ProfessionalAvailableDaysSerializer(serializers.Serializer):

    week_day = serializers.IntegerField(allow_null=False, help_text="el día de la semana que se quiere modificar")
    exclude = serializers.ListField(allow_null=False, help_text="las horas que se quiere excluir")

    def validate(self, attrs:dict):
        week_day = attrs.get("week_day")
        exclude = attrs.get("exclude")

        if week_day < 1 or week_day > 7:
            raise serializers.ValidationError(_("week_day must be between 1 and 7"))
        
        if len(exclude) > 0:
            for time_range in exclude:
                if len(time_range) != 2:
                    raise serializers.ValidationError(_("time_range must be a list of two elements"))
                if time_range[0] < 0 or time_range[0] > 23:
                    raise serializers.ValidationError(_("time_range must be between 0 and 23"))
                if time_range[1] < 0 or time_range[1] > 23:
                    raise serializers.ValidationError(_("time_range must be between 0 and 23"))
                if time_range[0] > time_range[1]:
                    raise serializers.ValidationError(_("time_range[0] must be less than time_range[1]"))
        
        return super().validate(attrs)

    


class PlacePutSerializer(serializers.Serializer):
    place_id = serializers.IntegerField(allow_null=False, help_text="el id del lugar que ser quiere modificar")
    place_data = serializers.JSONField(allow_null=False, help_text="los datos del lugar que se quiere modificar")
    days_data = serializers.JSONField(allow_null=True, help_text="los datos de los días que se quiere modificar")



class OrganizationClientPutSerializer(serializers.Serializer):

    client_id = serializers.IntegerField(required=True, help_text='Client id')
    client_data = OrganizationClientSerializer(required=True, help_text='Client data')


class OrganizationProfessionalPostBodySerializer(serializers.Serializer):

    email = serializers.EmailField(required=True, help_text='Email of the professional')
    first_name = serializers.CharField(required=True, help_text='First name of the professional')
    last_name = serializers.CharField(required=True, help_text='Last name of the professional')
    phone = serializers.CharField(required=True, help_text='Phone of the professional')
    username = serializers.CharField(required=True, help_text='Username of the professional')
    organization = serializers.CharField(required=True, help_text='Organization id of the professional')
    password = serializers.CharField(required=True, help_text='Password of the professional')


class OrganizationProfessionalPutBodySerializer(serializers.Serializer):

    professional_id = serializers.IntegerField(required=True, help_text='Professional id')
    professional_data = OrganizationProfessionalSerializer(required=True, help_text='Professional data')
    days = serializers.ListField(allow_null=True, help_text='Days data', child=ProfessionalAvailableDaysSerializer())


    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)


    def __convert_to_objects(self, attrs):
        try:
            attrs['professional'] = OrganizationProfessional.objects.get(id=attrs['professional_id'])
        except OrganizationProfessional.DoesNotExist:
            raise serializers.ValidationError(_('Professional does not exist'))
        