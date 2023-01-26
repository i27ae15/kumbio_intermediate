from rest_framework import serializers


class VerifyCodeToRecoverPasswordQuerySerializer(serializers.Serializer):
    code = serializers.CharField(required=True)