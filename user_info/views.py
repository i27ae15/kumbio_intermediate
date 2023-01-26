# python
# django 
# rest-framework
from django.utils.translation import gettext_lazy as _

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Swagger
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# models 
from user_info.models import KumbioUser, NotificationsSettings

# serializers 
from .serializers.serializers import KumbioUserSerializer, KumbioUserAvailablePlacesSerializer, KumbioUserAvailableServicesSerializer, NotificationsSettingsSerializer
from .serializers.body_serializers import ChangePasswordBodySerializer, RecoverPasswordBodySerializer
from .serializers.query_serializers import VerifyCodeToRecoverPasswordQuerySerializer

# others
from print_pp.logging import Print


@swagger_auto_schema(
    method='get',
    query_serializer=VerifyCodeToRecoverPasswordQuerySerializer,
    operation_description="""Obtiene la información de un usuario
        query parameters:
        code: código de recuperación de contraseña
    """,
    responses={
        200: 'True si el código es válido',
        400: 'Error en los datos',
    },
    tags=['password'])
@api_view(['GET'])
def verify_recovery_password_code(request):

    query_serializer = VerifyCodeToRecoverPasswordQuerySerializer(data=request.query_params)
    query_serializer.is_valid(raise_exception=True)
    query_data = query_serializer.validated_data

    try: KumbioUser.objects.get(code_to_recover_password=query_data['code'])
    except KumbioUser.DoesNotExist: raise exceptions.PermissionDenied(_('Código inválido'))
    return Response({'is_valid_code': True})


@swagger_auto_schema(
    method='post',
    request_body=ChangePasswordBodySerializer,
    operation_description="Change password",
    responses={
        200: 'Contraseña cambiada',
        400: 'Error en los datos',
    },
    tags=['password'])
@api_view(['POST'])
def change_password(request):
    body_serializer = ChangePasswordBodySerializer(data=request.data)
    body_serializer.is_valid(raise_exception=True)
    body_data = body_serializer.validated_data

    user:KumbioUser = body_data['user']
    user.change_password(body_data['new_password'])
    return Response({'message': 'Contraseña cambiada'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=RecoverPasswordBodySerializer, 
    operation_description="Recupera la contraseña de un usuario",
    responses={
        200: 'Email enviado',
    },
    tags=['password'])
@api_view(['POST'])
def recover_password(request):
    body_serializer = RecoverPasswordBodySerializer(data=request.data)
    body_serializer.is_valid(raise_exception=True)
    body_data = body_serializer.validated_data

    user:KumbioUser = body_data['user']
    user.send_password_recover_email()
    
    return Response({'message': 'Email enviado'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def authenticate_user(request):
    
    try:    
        calendar_token:str = request.data['calendar_token']
    except KeyError:
        return Response({'error': 'calendar_token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    try: KumbioUser.objects.get(calendar_token=calendar_token)
    except: return Response({'is_valid_user': False})
    return Response({'is_valid_user': True})


@swagger_auto_schema()
@api_view(['GET'])
def get_available_places_for_user(request):

    user_id = request.GET.get('user_id')

    try: user:KumbioUser = KumbioUser.objects.get(id=user_id)
    except KumbioUser.DoesNotExist: return Response({'error':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    available_places = KumbioUserAvailablePlacesSerializer(user)

    return Response(available_places.data, status=status.HTTP_200_OK)


@swagger_auto_schema()
@api_view(['GET'])
def get_available_services_for_user(request):

    user_id = request.GET.get('user_id')

    try: user:KumbioUser = KumbioUser.objects.get(id=user_id)
    except KumbioUser.DoesNotExist: return Response({'error':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    available_services = KumbioUserAvailableServicesSerializer(user)

    return Response(available_services.data, status=status.HTTP_200_OK)


@swagger_auto_schema()
@api_view(['GET'])
def get_kumbio_user(request):

    user_id = request.GET.get('user_id')

    try: user:KumbioUser = KumbioUser.objects.get(id=user_id)
    except KumbioUser.DoesNotExist: return Response({'error':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    available_places = KumbioUserSerializer(user)

    return Response(available_places.data, status=status.HTTP_200_OK)


class NotificationsSettingsView(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 

    
    def get(self, request):
        
        settings:NotificationsSettings = request.user.notifications_settings
        serializer = NotificationsSettingsSerializer(settings)

        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=NotificationsSettingsSerializer(),
    )
    def put(self, request):
        
        settings:NotificationsSettings = request.user.notifications_settings
        serializer = NotificationsSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)