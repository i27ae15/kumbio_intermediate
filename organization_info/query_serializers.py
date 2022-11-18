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
