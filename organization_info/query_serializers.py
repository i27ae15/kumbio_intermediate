from rest_framework import serializers

class PlaceQuerySerializer(serializers.Serializer):
        
    place_id = serializers.IntegerField(default=None, allow_null=True, help_text="el id del lugar quer ser quiere, por defecto es None, \
                                        lo cual traera todos los lugares que la organizacion tenga ligados")


class OrganizationProfessionalQuerySerializer(serializers.Serializer):
        
    kumbio_user_id = serializers.IntegerField(default=None, allow_null=True, help_text="el id del usuario de kumbio ligado al profesional que se quiere, por defecto es None, \
                                            lo cual traera todos los profesionales que la organizacion tenga ligados, (para poder traer a todos los profesionales \
                                            y a un usuario diferente al de la peticion, el usuario debe ser admin)")