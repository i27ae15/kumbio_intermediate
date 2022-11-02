# python

# django
from django.utils import timezone
from django.db.models import Q
from django.db.models.query import QuerySet

# rest-framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# models
from user_info.models import KumbioUser
from .models.main_models import Organization, OrganizationProfessional

# serializers
from user_info.serializers import KumbioUserSerializer, CreateKumbioUserSerializer
from .serializers import OrganizationProfessionalSerializer

# others
from print_pp.logging import Print



class OrganizationProfessionalAPI(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    
    def post(self, request):
        
        """

            OrganizationProfessional class inherits from KumbioUser, so to be able to create a new professional we got 
            to have a KumbioUser to inherits from, that's so we need to create it before the creation of the professional
        
            body parameters:

                email (str): email of the professional
                first_name (str): first name of the professional
                last_name (str): last name of the professional
                phone (str): phone of the professional
                username (str): username of the professional
                organization (str): organization id of the professional
        
        """
        
        # First we create the KumbioUser
        kumbio_user_serializer = CreateKumbioUserSerializer(data=request.data, context={'set_verified_email': True})
        
        if not kumbio_user_serializer.is_valid():
            return Response(kumbio_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        kumbio_user_serializer.save()
        kumbio_user:KumbioUser = kumbio_user_serializer.instance
        
        request.data['created_by_id'] = request.user.id
        request.data['kumbio_user_id'] = kumbio_user.id
        
        professional_serializer = OrganizationProfessionalSerializer(data=request.data)
        
        if not professional_serializer.is_valid():
            return Response(professional_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Print('before save')
        professional_serializer.save()
        Print('after save')
        professional:OrganizationProfessional = professional_serializer.instance
        
        
        return Response(professional_serializer.data, status=status.HTTP_201_CREATED)
        
        
    