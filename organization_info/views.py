# python
import requests
import os

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
from user_info.models import KumbioUser, KumbioUserRole
from .models.main_models import Organization, OrganizationProfessional, OrganizationPlace

# serializers
from user_info.serializers import CreateKumbioUserSerializer

from .query_serializers import PlaceQuerySerializer, OrganizationProfessionalQuerySerializer
from .serializers import OrganizationProfessionalSerializer, OrganizationPlaceSerializer, OrganizationSerializer

# others
from print_pp.logging import Print
from dotenv import load_dotenv
from user_info.info import ADMIN_ROLE_ID, PROFESSIONAL_ROLE_ID

load_dotenv()


CALENDAR_ENDPOINT = os.environ['CALENDAR_ENDPOINT']


# Functions

def check_if_user_is_admin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.role.id == ADMIN_ROLE_ID:
            return func(self, request, *args, **kwargs)
        else:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


def check_if_user_is_admin(request) -> 'True | Response':
    if request.user.role.id == ADMIN_ROLE_ID:
        return True
    else:
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)

# classes

class OrganizationView(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_description="Get organization",
        responses={
            200: openapi.Response(
                description="Organization",
                schema=OrganizationSerializer
            )
        }
    )
    def get(self, request):

        organization_id = request.GET.get('organization_id')

        if not organization_id:
            return Response({"message": "organization_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            organization_id = int(organization_id)
        except ValueError:
            return Response({"message": "organization_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)


        organization = Organization.objects.get(pk=organization_id)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_description="Update organization",
        request_body=OrganizationSerializer,
        responses={
            200: openapi.Response(
                description="Organization",
                schema=OrganizationSerializer
            )
        }
    )
    def put(self, request):
        organization = Organization.objects.get(pk=request.user.organization.id)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete organization",
        responses={
            200: openapi.Response(
                description="Organization",
                schema=OrganizationSerializer
            )
        }
    )
    def delete(self, request):
        organization = Organization.objects.get(pk=request.user.organization.id)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizationProfessionalAPI(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        query_serializer=OrganizationProfessionalQuerySerializer()
    )
    def get(self, request):
        """
            Get all the professionals of the organization
        """

        query_serializer = OrganizationProfessionalQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        if not query_params['kumbio_user_id']:
            # check if the user is an admin
            if check_if_user_is_admin(request) != True:
                return check_if_user_is_admin(request)

            # if the user is an admin, then we get all the professionals
            organization_professionals = OrganizationProfessional.objects.filter(organization__id=request.user.organization.id)

        else:
            
            # check if the user is the professional they are asking for
            if request.user.id != query_params['kumbio_user_id']:
                if check_if_user_is_admin(request) != True:
                    return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
                    
            organization_professionals = OrganizationProfessional.objects.filter(kumbio_user__id=int(query_params['kumbio_user_id']))

        serializer = OrganizationProfessionalSerializer(organization_professionals, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
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


        # we should handle this petition that if not successfully delete the created user, due to the fact that this cannot continue
        res = requests.post(f'{CALENDAR_ENDPOINT}register/api/v2/create-user/', json={
                'organization_id': request.data['organization_id'],
                'email':request.data['email'],
                'first_name': request.data['first_name'],
                'last_name': request.data['last_name'],
                'role': PROFESSIONAL_ROLE_ID, 
            })
        
        if not kumbio_user_serializer.is_valid():
            return Response(kumbio_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        kumbio_user_serializer.save()
        kumbio_user:KumbioUser = kumbio_user_serializer.instance
        
        # somehow this information is not getting saved within the serializer, so we have to do it manually
        kumbio_user.role = KumbioUserRole.objects.get(id=PROFESSIONAL_ROLE_ID) # getting the role as organization_professional
        kumbio_user.organization = Organization.objects.get(id=request.data['organization_id'])
        kumbio_user.calendar_token = res.json()['token']
        kumbio_user.set_password(request.data['password'])
        kumbio_user.save()
        
        request.data['created_by_id'] = request.user.id
        request.data['kumbio_user_id'] = kumbio_user.id
        
        professional_serializer = OrganizationProfessionalSerializer(data=request.data)
        
        if not professional_serializer.is_valid():
            return Response(professional_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        professional_serializer.save()
            
        return Response(professional_serializer.data, status=status.HTTP_201_CREATED)
        
        
class OrganizationPlaceAPI(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 


    @swagger_auto_schema(
        query_serializer=PlaceQuerySerializer(),
    )
    def get(self, request):
        """
            Get places 
        """

        query_serializer = PlaceQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.data

        if query_params['place_id']:
            places = self.check_if_place_exists(request.user, int(query_params['place_id']))

            if places:
                place_serializer = OrganizationPlaceSerializer(places)
            else:
                return Response(
                    {
                        'error': 'el lugar no existe'
                    }, status=status.HTTP_404_NOT_FOUND)

        else:
            places = OrganizationPlace.objects.filter(organization=request.user.organization.id)
            place_serializer = OrganizationPlaceSerializer(places, many=True)
        
        return Response(place_serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body = OrganizationPlaceSerializer(),
        responses={200: OrganizationPlaceSerializer()},
    )
    @check_if_user_is_admin_decorator
    def post(self, request):
        """
            Create a new Place
            Solo los administradores pueden crear lugares
        """
        request.data['organization'] = request.user.organization.id
        request.data['created_by'] = request.user.id
        
        place_serializer = OrganizationPlaceSerializer(data=request.data)
    
        if place_serializer.is_valid():
            place_serializer.save()

            return Response(place_serializer.data, status.HTTP_201_CREATED)
        
        return Response(place_serializer.errors, status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        request_body = OrganizationPlaceSerializer(),
        responses={200: OrganizationPlaceSerializer()},
    )
    @check_if_user_is_admin_decorator
    def put(self, request):
        """
        Update a Place
        """
        try:

            place = self.check_if_place_exists(request.user, request.data['place_id'])

            if not place:
                return Response(
                    {
                        'error': 'el lugar no existe'
                    }, status=status.HTTP_404_NOT_FOUND)

        except KeyError:
            return Response(
                {
                    'error': 'place_id es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)

        place_serializer = OrganizationPlaceSerializer(place, data=request.data)
        
        if place_serializer.is_valid():
            place_serializer.save()
            return Response(place_serializer.data, status=status.HTTP_200_OK)
        
        return Response(place_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    @swagger_auto_schema(
    request_body= openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'place_id': openapi.Schema(
            type=openapi.TYPE_INTEGER, 
            description='id del place que ser quiere eliminar'),
        'delete_calendars': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='indica si se quiere eliminar los calendarios asociados al place', default=False),
    },
    required=['place_id']))
    @check_if_user_is_admin_decorator
    def delete(self, request):
        """
        Delete a Place
        """
        try:

            place = self.check_if_place_exists(request.user, request.data['place_id'])

            if not place:
                return Response(
                {
                    'error': 'el lugar no existe'
                }, status=status.HTTP_404_NOT_FOUND)

        except KeyError:
            return Response(
                {
                    'error': 'place_id es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)


        if not request.data.get('delete_calendars'):
            # TODO: Perform communication with calendar api to delete calendars
            calendars:Calendar = place.get_calendars()

            for calendar in calendars:
                calendar:Calendar
                calendar.clear_place()

        place.delete()

        return Response({'message': 'lugar eliminado'}, status=status.HTTP_200_OK)
    

    def check_if_place_exists(self, user, place_id):

        try:
            place:OrganizationPlace = OrganizationPlace.objects.get(organization=user.organization.id, id=place_id)
            return place

        except OrganizationPlace.DoesNotExist:
            return False


