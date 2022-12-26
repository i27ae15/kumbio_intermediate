from rest_framework import serializers

from organization_info.utils.validators import get_places

from django.utils.translation import gettext_lazy as _

from print_pp.logging import Print

class OrganizationQuerySerializer(serializers.Serializer):
        
    organization_id = serializers.CharField( 
        allow_null=False,
        help_text="el id de la organización que se quiere")


class OrganizationProfessionalQuerySerializer(serializers.Serializer):
        
    kumbio_user_id = serializers.IntegerField(default=None, allow_null=True, help_text="el id del usuario de kumbio ligado al profesional que se quiere, por defecto es None, \
                                            lo cual traerá todos los profesionales que la organización tenga ligados, (para poder traer a todos los profesionales \
                                            y a un usuario diferente al de la petición, el usuario debe ser admin)")

    organization_id = serializers.IntegerField(default=None, allow_null=True, help_text="el id de la organización que se quiere, por defecto es None, \
                                            lo cual traerá todos los profesionales que la organización tenga ligados, (para poder traer a todos los profesionales \
                                            y a un usuario diferente al de la petición, el usuario debe ser admin)")

    def validate(self, attrs):
        if not attrs['kumbio_user_id'] and not attrs['organization_id']:
            raise serializers.ValidationError(_("Si no hay un kumbio_user_id, se debe enviar el id de la organización"))
        return super().validate(attrs)

class OrganizationSectorQuerySerializer(serializers.Serializer):
        
    sector_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id del sector que se quiere obtener \
                                        si se deja en blanco se obtienen todos los sectores")


class OrganizationServiceQuerySerializer(serializers.Serializer):
        
    service_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id del servicio que se quiere obtener \
                                        si se deja en blanco se obtienen todos los servicios")
    

class OrganizationClientQuerySerializer(serializers.Serializer):
        
    client_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id del cliente que se quiere obtener \
                                        si se deja en blanco se obtienen todos los clientes")
    
    min_age = serializers.IntegerField(default=0, help_text="Edad mínima del cliente que se quiere obtener, al dejarse en Nono trae todos")
    max_age = serializers.IntegerField(default=999, help_text="Edad máxima del cliente que se quiere obtener, al dejarse en Nono trae todos")
    
    min_rating = serializers.IntegerField(default=0, help_text="Calificación mínima del cliente que se quiere obtener")
    max_rating = serializers.IntegerField(default=5, help_text="Calificación máxima del cliente que se quiere obtener")
    
    birth_date = serializers.DateField(default=None, allow_null=True, help_text="Fecha de nacimiento del cliente que se quiere obtener")


class OrganizationClientTypeQuerySerializer(serializers.Serializer):
        
    client_type_id = serializers.IntegerField(default=None, allow_null=True, help_text="Id del tipo de cliente que se quiere obtener, por defecto es None, \
                                            lo cual traerá todos los tipos de cliente que la organización tenga ligados")


class OrganizationPlaceQuerySerializer(serializers.Serializer):
        
    place_id = serializers.IntegerField(
        default=None, 
        allow_null=True, 
        help_text="Id del lugar que se quiere obtener, por defecto es None, \
        lo cual traerá todos los lugares que la organización tenga ligados"
    )


    def validate(self, attrs:dict):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)

    
    def __convert_to_objects(self, attrs:dict):

        attrs['places'] = get_places(
            organization = self.context['organization'], 
            place_id = attrs['place_id'], 
            return_as_query_set=True)