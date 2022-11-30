# python
import requests
import os

# django
from django.utils import timezone
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

# rest-framework
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# models
from user_info.models import KumbioUser, KumbioUserRole
from .models.main_models import (Organization, OrganizationProfessional, OrganizationPlace, Sector, 
OrganizationService, OrganizationClientCreatedBy, DayAvailableForPlace, DayName)

# serializers
from user_info.serializers import CreateKumbioUserSerializer

from .query_serializers import PlaceQuerySerializer, OrganizationProfessionalQuerySerializer, OrganizationSectorQuerySerializer, OrganizationServiceQuerySerializer
from .serializers import (OrganizationProfessionalSerializer, OrganizationPlaceSerializer, OrganizationSerializer, OrganizationSectorSerializer, 
OrganizationServiceSerializer, DayAvailableForPlaceSerializer, OrganizationClientSerializer, OrganizationClientDependentFromSerializer)

# others
from authentication_manager.authenticate import KumbioAuthentication

from print_pp.logging import Print
from dotenv import load_dotenv
from user_info.info import ADMIN_ROLE_ID, PROFESSIONAL_ROLE_ID

load_dotenv()


CALENDAR_ENDPOINT = os.environ['CALENDAR_ENDPOINT']


# Functions

def check_if_user_is_admin_decorator(func, *args, **kwargs):
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

        # try:
        #     organization_id = int(organization_id)
        # except ValueError:
        #     return Response({"message": "organization_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)


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
        responses={200: OrganizationPlaceSerializer()},
    )
    def post(self, request):
        """
            Create a new Place
            Solo los administradores pueden crear lugares

            para esto es necesario pasar dos objectos uno de place, para crear el lugar y otro para los días que ese lugar acepta, iniciando con Monday = 0


            request body:

                place (object): {
                    address:str = 'string'
                    admin_email:str = 'string'
                    accepts_children:bool = true
                    accepts_pets:bool = true
                    additional_info:str = 'string'
                    after_hours_phone:str = 'string'

                    email:str = 'email@email.com'

                    google_maps_link:str = 'string'

                    important_information:str = 'string'

                    main_office_number:str = 'string'

                    name:str = 'string'

                    phone:str = 'string'

                    photo:str = 'string'
                    
                    local_timezone:str = 'string'
                    
                    # if this place has a custom price for a service
                    custom_price:list[dict] = [{
                        place_id: 1,
                        price: 25,
                    }]
                },

                days = [
                    {
                        week_day:int = 0 # donde Monday es = 0 y Sunday = 6
                        exclude:list = [[0, 7], [18, 23]], null=True, blank=True)
                        note:str = "Una nota de prueba"
                    }
                ]
        """
        request.data['place']['organization'] = request.user.organization.id
        request.data['place']['created_by'] = request.user.id
        
        place_serializer = OrganizationPlaceSerializer(data=request.data['place'])
    
        if place_serializer.is_valid():
            place_serializer.save()

            daysAvailable:list[dict] = request.data['days']

            if daysAvailable:
                for day in daysAvailable:
                    day['place'] = place_serializer.data['id']

                days_available_serializer = DayAvailableForPlaceSerializer(data=daysAvailable, many=True)
                if days_available_serializer.is_valid():
                    days_available_serializer.save()
                else:
                    return Response(days_available_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class OrganizationSectorView(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 

    
    @swagger_auto_schema(
        query_serializer=OrganizationSectorQuerySerializer(),
    )
    def get(self, request):

        qp = OrganizationSectorQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        query_params = qp.data
        
        if query_params['sector_id']:
            sectors = Sector.objects.filter(id=query_params['sector_id'])
            if not sectors:
                return Response(
                    {
                        'error': 'el sector no existe'
                    }, status=status.HTTP_404_NOT_FOUND)
        else:
            sectors = Sector.objects.all()


        sector_serializer = OrganizationSectorSerializer(sectors, many=True)
        return Response(sector_serializer.data, status=status.HTTP_200_OK)


class OrganizationServiceView(APIView):
    
        permission_classes = (IsAuthenticated,) 
        authentication_classes = (TokenAuthentication,) 
    
        
        @swagger_auto_schema(
            query_serializer=OrganizationServiceQuerySerializer(),
        )
        def get(self, request):
    
            qp = OrganizationServiceQuerySerializer(data=request.query_params)
            qp.is_valid(raise_exception=True)
            query_params = qp.data
            
            if query_params['service_id']:
                services = OrganizationService.objects.filter(id=query_params['service_id'])
                if not services:
                    return Response(
                        {
                            'error': 'el servicio no existe'
                        }, status=status.HTTP_404_NOT_FOUND)
            else:
                services = OrganizationService.objects.all()
    
    
            service_serializer = OrganizationServiceSerializer(services, many=True)
            return Response(service_serializer.data, status=status.HTTP_200_OK)
        
        @swagger_auto_schema(
            request_body=OrganizationServiceSerializer(),
        )
        def post(self, request):
            """
                Create a new Service
                Solo los administradores pueden crear servicios
            """
            request.data['organization'] = request.user.organization.id
            request.data['created_by'] = request.user.id
            
            service_serializer = OrganizationServiceSerializer(data=request.data)
        
            if service_serializer.is_valid():
                service_serializer.save()
    
                return Response(service_serializer.data, status.HTTP_201_CREATED)
            
            return Response(service_serializer.errors, status.HTTP_400_BAD_REQUEST)


class OrganizationClientView(APIView):

    # this needs authorization from calendar
    # we need to create an authorization token for the calendar api to be able to access this endpoint
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (KumbioAuthentication,)

    @swagger_auto_schema(
        request_body=OrganizationClientSerializer(),
    )
    def post(self, request):
        
        # getting the data from the request that comes "separated"
        client_data:dict = request.data['client']
        dependent_from:dict = request.data['dependent_from']
        client_data['created_by'] = request.user.app

        client_serializer = OrganizationClientSerializer(data=client_data)
        
        if client_serializer.is_valid():
            client_serializer.save()
            dependent_from['client'] = client_serializer.data['id']

            if dependent_from.get('same_as_client'):
                new_data = {
                    'first_name': client_data['first_name'],
                    'last_name': client_data['last_name'],
                    'email': client_data['email'],
                    'phone': client_data['phone'],
                    'phone2': client_data.get('phone2', None),
                }
                dependent_from.update(new_data)
                
            else:
                dependent_from['same_as_client'] = False

            dependent_from_serializer = OrganizationClientDependentFromSerializer(data=dependent_from)
            
            if dependent_from_serializer.is_valid():
                dependent_from_serializer.save()
            else:
                return Response(dependent_from_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(client_serializer.data, status.HTTP_201_CREATED)
        
        return Response(client_serializer.errors, status.HTTP_400_BAD_REQUEST)

