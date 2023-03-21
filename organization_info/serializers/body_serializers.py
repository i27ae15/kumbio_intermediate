from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from .model_serializers import (
    ClientParentSerializer, OrganizationClientSerializer, OrganizationProfessionalSerializer, 
    OrganizationPlaceSerializer
)
from organization_info.models.main_models import (
    DayAvailableForPlace, Organization, OrganizationClient, OrganizationClientDocument, OrganizationProfessional, OrganizationService, DayAvailableForProfessional
)

from organization_info.utils.validators import get_places



# private serializers
# these serializers are used to validate a dict that comes within the properties of another serializer
class AvailableDaysPrivateSerializer(serializers.Serializer):

    week_day = serializers.IntegerField(required=True, help_text="el día de la semana que se quiere modificar")
    exclude = serializers.ListField(required=False, help_text="las horas que se quiere excluir")
    service = serializers.DictField(required=False, help_text="el servicio que se quiere agregar")
    note = serializers.CharField(required=False, help_text="la nota que se quiere agregar")

    def validate(self, attrs:dict):
        week_day = attrs.get("week_day")
        exclude = attrs.get("exclude")

        if week_day < 0 or week_day > 6:
            raise serializers.ValidationError(_("week_day must be between 0 and 6, where 0 is Monday and 6 is Sunday"))
        
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


class KumbioUserPrivateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_null=True, help_text="el nombre del usuario")
    last_name = serializers.CharField(required=False, allow_null=True, help_text="el apellido del usuario")
    email = serializers.EmailField(required=False, allow_null=True, help_text="el email del usuario")
    phone = serializers.CharField(required=False, allow_null=True, help_text="el teléfono del usuario")


# public serializers

# serializers for put requests
class PlacePutSerializer(serializers.Serializer):
    place_id = serializers.IntegerField(allow_null=False, required=True, help_text="el id del lugar que ser quiere modificar")
    place_data = serializers.JSONField(allow_null=False, help_text="los datos del lugar que se quiere modificar")
    days_data = serializers.JSONField(allow_null=True, default=None, help_text="los datos de los días que se quiere modificar")


    def validate(self, attrs):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)

    
    def __convert_to_objects(self, attrs:dict):
        attrs['place'] = get_places(self.context['organization'], attrs['place_id'])


class OrganizationClientPutSerializer(serializers.Serializer):

    client_id = serializers.IntegerField(required=True, help_text='Client id')
    client_data = OrganizationClientSerializer(required=True, help_text='Client data')


class OrganizationClientDeleteSerializer(serializers.Serializer):

    client_id = serializers.IntegerField(required=True, help_text='Client id')


class OrganizationProfessionalPutBodySerializer(serializers.Serializer):

    professional_id = serializers.IntegerField(required=True, help_text='Professional id')
    professional_data = OrganizationProfessionalSerializer(default=dict, help_text='Professional data', partial=True)
    kumbio_user_data = KumbioUserPrivateSerializer(default=dict, help_text='Kumbio user data', partial=True)
    days = serializers.ListField(allow_null=True, required=False, help_text='Days data', child=AvailableDaysPrivateSerializer())


    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)


    def __convert_to_objects(self, attrs):
        try:
            attrs['professional'] = OrganizationProfessional.objects.get(id=attrs['professional_id'])
        except OrganizationProfessional.DoesNotExist:
            raise serializers.ValidationError(_('Professional does not exist'))
        

# serializers for post requests
class OrganizationProfessionalPostBodySerializer(serializers.Serializer):

    email = serializers.EmailField(required=True, help_text='Email of the professional')
    first_name = serializers.CharField(required=True, help_text='First name of the professional')
    last_name = serializers.CharField(required=True, help_text='Last name of the professional')
    phone = serializers.CharField(required=True, help_text='Phone of the professional')
    username = serializers.CharField(required=True, help_text='Username of the professional')
    organization = serializers.CharField(required=True, help_text='Organization id of the professional')
    password = serializers.CharField(required=True, help_text='Password of the professional')
    place_id = serializers.IntegerField(required=True, help_text='Place id of the professional')


class OrganizationPlacePostSerializer(serializers.Serializer):

    place = OrganizationPlaceSerializer(required=True, help_text='Place data')
    days = serializers.ListField(allow_null=True, help_text='Days data', child=AvailableDaysPrivateSerializer())

    def validate(self, attrs:dict):

        attrs['place']['organization'] = self.context['organization']
        attrs['place']['created_by'] = self.context['created_by']    

        return super().validate(attrs)


class OrganizationClientForCalendarBodySerializer(serializers.Serializer):

    client_parent = ClientParentSerializer(required=True, help_text='Parent data')
    client = serializers.DictField(required=True, help_text='Client data')
    organization_id = serializers.CharField(required=True, help_text='Organization id of the parent')

    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)
    

    def __convert_to_objects(self, attrs:dict):
        try:
            attrs['organization'] = Organization.objects.get(id=attrs['organization_id'])
        except Organization.DoesNotExist:
            raise serializers.ValidationError(_('Organization does not exist'))
        

class IncrementNumberOfAppointmentsBodySerializer(serializers.Serializer):

    organization_id = serializers.CharField(required=True, help_text='Organization id')
    service_id = serializers.IntegerField(required=True, help_text='Service id')


    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)
    

    def __convert_to_objects(self, attrs:dict):
        try:
            attrs['organization'] = Organization.objects.get(id=attrs['organization_id'])
        except Organization.DoesNotExist:
            raise serializers.ValidationError(_('Organization does not exist'))
        
        try:
            attrs['service'] = OrganizationService.objects.get(id=attrs['service_id'])
        except OrganizationService.DoesNotExist:
            raise serializers.ValidationError(_('Service does not exist'))
    

# serializers for delete requests

class OrganizationProfessionalDeleteBodySerializer(serializers.Serializer):

    professional_id = serializers.IntegerField(required=True, help_text='Professional id')


    def validate(self, attrs:dict):
        self.convert_to_objects(attrs)
        return super().validate(attrs)


    def convert_to_objects(self, attrs):
        try:
            attrs['professional'] = OrganizationProfessional.objects.get(id=attrs['professional_id'])
        except OrganizationProfessional.DoesNotExist:
            raise serializers.ValidationError(_('Professional does not exist'))


class DeleteServiceSerializer(serializers.Serializer):

    service_id = serializers.IntegerField(required=True, help_text='Service id')


    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)


    def __convert_to_objects(self, attrs):
        try:
            attrs['service'] = OrganizationService.objects.get(id=attrs['service_id'], deleted_at__isnull=True)
        except OrganizationService.DoesNotExist:
            raise serializers.ValidationError(_('Service does not exist'))
        

class DeleteDayAvailableForProfessionalSerializer(OrganizationProfessionalDeleteBodySerializer):

    week_day = serializers.IntegerField(required=True, help_text='dia de la semana')


    def validate(self, attrs:dict):
        self.convert_to_objects(attrs)
        return super().validate(attrs)


    def convert_to_objects(self, attrs):
        super().convert_to_objects(attrs)
        try:
            professional:OrganizationProfessional = attrs['professional']
            attrs['day'] = professional.available_days.get(week_day=attrs['week_day'])
        except DayAvailableForProfessional.DoesNotExist:
            raise serializers.ValidationError(_('Day does not exist'))
        

class DeleteDayAvailableForPlaceSerializer(serializers.Serializer):

    day_id = serializers.IntegerField(required=True, help_text='Day id')


    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)


    def __convert_to_objects(self, attrs):
        try:
            attrs['day_id'] = DayAvailableForPlace.objects.get(week_day=attrs['week_day'])
        except DayAvailableForPlace.DoesNotExist:
            raise serializers.ValidationError(_('Day does not exist'))


class DeleteClientDocumentSerializer(serializers.Serializer):

    document_id = serializers.IntegerField(required=True, help_text='Document id')
    client_id = serializers.IntegerField(required=True, help_text='Client id')


    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)


    def __convert_to_objects(self, attrs):
        client:OrganizationClient = OrganizationClient.objects.get(id=attrs['client_id'])
        
        try: attrs['document'] = client.documents_associated.get(id=attrs['document_id'])
        except OrganizationClientDocument.DoesNotExist: raise serializers.ValidationError(_('Document does not exist'))

