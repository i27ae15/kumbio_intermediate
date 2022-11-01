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
from organization_info.models.email_template_models import MailTemplate, MailTemplatesManager

# serializers 
from organization_info.serializers import OrganizationSerializer
from user_info.serializers import UserCustomSerializer, CreateUserSerializer


# others


@api_view(['GET'])
def authenticate_user(request):
    
    calendar_token:str = request.data['calendar_token']
    
    try: KumbioUser.objects.get(calendar_token=calendar_token)
    except: return Response({'exists': False})
    return Response({'exists': True})

