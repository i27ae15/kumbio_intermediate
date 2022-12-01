# python
# django 
# rest-framework
from rest_framework import status

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
from .serializers import KumbioUserSerializer, KumbioUserAvailablePlacesSerializer, KumbioUserAvailableServicesSerializer, NotificationsSettingsSerializer


# others
from print_pp.logging import Print


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