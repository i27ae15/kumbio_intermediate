from rest_framework import serializers

class PlacePutSerializer(serializers.Serializer):
    place_id = serializers.IntegerField(allow_null=False, help_text="el id del lugar que ser quiere modificar")
    place_data = serializers.JSONField(allow_null=False, help_text="los datos del lugar que se quiere modificar")
    days_data = serializers.JSONField(allow_null=True, help_text="los datos de los días que se quiere modificar")
