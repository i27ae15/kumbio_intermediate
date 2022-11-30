from rest_framework import serializers

class PlaceQuerySerializer(serializers.Serializer):
        
    place_id = serializers.IntegerField(default=None, allow_null=True, help_text="el id del lugar que ser quiere, por defecto es None, \
                                        lo cual traerá todos los lugares que la organización tenga ligados")


class OrganizationProfessionalQuerySerializer(serializers.Serializer):
        
    kumbio_user_id = serializers.IntegerField(default=None, allow_null=True, help_text="el id del usuario de kumbio ligado al profesional que se quiere, por defecto es None, \
                                            lo cual traerá todos los profesionales que la organización tenga ligados, (para poder traer a todos los profesionales \
                                            y a un usuario diferente al de la petición, el usuario debe ser admin)")


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