from email.policy import default
from rest_framework import serializers

class PlaceQuerySerializer(serializers.Serializer):
        
    place_id = serializers.IntegerField(default=None, allow_null=True, help_text="el id del lugar quer ser quiere, por defecto es None, \
                                        lo cual traera todos los lugares que la organizacion tenga ligados")