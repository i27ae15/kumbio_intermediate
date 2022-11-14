import requests
import os

# django 
import secrets
from django.contrib.auth import get_user_model # If used custom user model
from django.db.models.query import QuerySet

# rest-framework
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Swagger
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# models 
from user_info.models import KumbioUser
from organization_info.models.main_models import Organization

# serializers 
from organization_info.serializers import OrganizationSerializer
from .serializers import KumbioUserSerializer, CreateKumbioUserSerializer, KumbioUserAvailablePlaces


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
    
    available_places = KumbioUserAvailablePlaces(user)

    return Response(available_places.data, status=status.HTTP_200_OK)



@swagger_auto_schema()
@api_view(['GET'])
def get_kumbio_user(request):

    user_id = request.GET.get('user_id')

    try: user:KumbioUser = KumbioUser.objects.get(id=user_id)
    except KumbioUser.DoesNotExist: return Response({'error':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    available_places = KumbioUserSerializer(user)

    return Response(available_places.data, status=status.HTTP_200_OK)
