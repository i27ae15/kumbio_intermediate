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
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# models
from user_info.models import KumbioUser, KumbioUserRole
from .models.main_models import (Organization, OrganizationProfessional, OrganizationPlace, Sector, 
OrganizationService, OrganizationClient, OrganizationClientType)
from authentication_manager.models import KumbioToken

# serializers
from user_info.serializers import CreateKumbioUserSerializer

from .query_serializers import (PlaceQuerySerializer, OrganizationProfessionalQuerySerializer, OrganizationSectorQuerySerializer, 
OrganizationServiceQuerySerializer, OrganizationClientQuerySerializer, OrganizationClientTypeQuerySerializer)

from .put_serializers import PlacePutSerializer

from .serializers import (OrganizationProfessionalSerializer, OrganizationPlaceSerializer, OrganizationSerializer, OrganizationSectorSerializer, 
OrganizationServiceSerializer, DayAvailableForPlaceSerializer, OrganizationClientSerializer, OrganizationClientDependentFromSerializer,
OrganizationClientTypeSerializer)


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
        
        if res.status_code != 201 or 'token' not in res.json():
            return Response({"error": res.json()}, status=status.HTTP_400_BAD_REQUEST)
        
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

            daysAvailable:list[dict] = request.data.get('days')

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
        request_body = PlacePutSerializer(),
        responses={200: OrganizationPlaceSerializer()},
    )
    @check_if_user_is_admin_decorator
    def put(self, request):
        """

            Si se quiere añadir otro dia al lugar, se hace desde aquí, añadiendo el dia a la lista de días disponibles

            place_data = OrganizationPlaceSerializer
            days_data = DayAvailableForPlaceSerializer
            days = [
                {
                    week_day:int = 0 # donde Monday es = 0 y Sunday = 6
                    exclude:list = [[0, 7], [18, 23]], null=True, blank=True)
                    note:str = "Una nota de prueba"
                }
            ]

        Update a Place
        """
        # use here the same schema as the post method
        # TODO: when a schedule for a place is modified, this must modified also the schedule of the professionals that work in that place

        put_serializer = PlacePutSerializer(data=request.data)
        put_serializer.is_valid(raise_exception=True)
        put_data = put_serializer.data

        place = self.check_if_place_exists(request.user, put_data['place_id'])
        place_serializer = OrganizationPlaceSerializer(place, data=put_data['place_data'], partial=True)

        data_to_return = dict(place=dict(), days=list())
        
        if place_serializer.is_valid():
            place_serializer.save()
            data_to_return['place'] = place_serializer.data
        
        place_instance:OrganizationPlace = place_serializer.instance
        
        if put_data['days_data']:
            for day in put_data['days_data']:

                available_day = place_instance.get_day_available(day['week_day'])
                day_serializer = None

                if available_day:
                    day_serializer = DayAvailableForPlaceSerializer(available_day, data=day, partial=True)
                    day_serializer.is_valid(raise_exception=True)
                    day_serializer.save()
                else:
                    # this will mean that this day has not been created yet, so we have to create it
                    day_serializer = DayAvailableForPlaceSerializer(data=day)
                    day_serializer.is_valid(raise_exception=True)
                    day_serializer.save()
            
            data_to_return['days'].append(day_serializer.data)

        
        return Response(data_to_return, status=status.HTTP_200_OK)

        
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

        @swagger_auto_schema(
            request_body=OrganizationServiceSerializer(),
        )
        def put(self, request):

            """
                Update an existent Service
                Solo los administradores pueden actualizar servicios

                request body:

                    {
                        "service": OrganizationServiceSerializer
                        "service_id": int
                    }
            """

            try:
                service:OrganizationService = OrganizationService.objects.get(id=request.data['service_id'])
            except OrganizationService.DoesNotExist:
                raise exceptions.NotFound(_('el servicio no existe'))
            except KeyError:
                raise exceptions.ParseError(_('service_id es requerido'))

            
            data_for_serializer = request.data['service']
            service_serializer = OrganizationServiceSerializer(instance=service, data=data_for_serializer)
        
            if service_serializer.is_valid():
                service_serializer.save()
    
                return Response(service_serializer.data, status.HTTP_201_CREATED)
            
            return Response(service_serializer.errors, status.HTTP_400_BAD_REQUEST)

        
        @swagger_auto_schema()
        def delete(self, request):

            """
                Delete an existent Service
                Solo los administradores pueden eliminar servicios

                request body:

                    {
                        "service_id": int
                    }
            """

            # make connections with calendar api to check if there is any appointment with this service associated
            # if there is, return error, cause the user cannot delete a service if there is any appointment with it

            try:
                service:OrganizationService = OrganizationService.objects.get(id=request.data['service_id'])
            except OrganizationService.DoesNotExist:
                raise exceptions.NotFound(_('el servicio no existe'))
            except KeyError:
                raise exceptions.ParseError(_('service_id es requerido'))

            service.delete()
            return Response({'message': 'servicio eliminado'}, status=status.HTTP_200_OK)


class OrganizationClientView(APIView):

    # this needs authorization from calendar
    # we need to create an authorization token for the calendar api to be able to access this endpoint
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (KumbioAuthentication,)
    
    @swagger_auto_schema(
        query_serializer=OrganizationClientQuerySerializer(),
    )
    def get(self, request):
        """
            Get all clients
        """
        user:KumbioUser = None

        if isinstance(request.user, KumbioToken):
            raise exceptions.PermissionDenied(_('No tienes permiso para realizar esta acción'))

        user = request.user
        
        query_serializer = OrganizationClientQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        if query_params['client_id']:
            clients:QuerySet[OrganizationClient] = OrganizationClient.objects.filter(id=query_params['client_id'], organization=request.user.organization.id)
            if not clients:
                raise exceptions.NotFound(_('el cliente no existe'))

        else: 
            clients:QuerySet[OrganizationClient] = OrganizationClient.objects.filter(organization=user.organization.id)
            Print('age', clients[0].age)
            
            clients = clients.filter(age__gte=query_params['min_age'],
                           age__lte=query_params['max_age'],
                           rating__gte=query_params['min_rating'],
                           rating__lte=query_params['max_rating'])
            
            Print('clients', clients)
            
            if query_params['birth_date']:
                clients = clients.filter(birth_date=query_params['birth_date'])

        client_serializer = OrganizationClientSerializer(clients, many=True)
        return Response(client_serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema()
    def post(self, request):

        """
        
        la información debe venir separada en dos objectos JSON, uno para el cliente y otro para el 
        dependiente, si no hay dependiente, el segundo objeto debe solo tener un propiedad llamada
        same_as_client con valor True

        los campos para llenar el "extra_fields" los obtienes de organization/client_types/


        request body:

            {
                client: {
                    "type" (int) (required): client_type_id,
                    "first_name" (str) (required): "nombre",
                    "last_name" (str) (required): "apellido",
                    "extra_fields" (array) (required): [
                        ('pets_first_name', FieldType.TEXT, 'Juan Carlos'), 
                        ('pets_last_name', FieldType.TEXT, 'Atrida')
                    ],
                    "birthday" (str): "YYYY-MM-DD", 
                    "comments" (str): "comentarios",
                    "identification" (str): "identificación",
                    "age" (int): 25,
                    "rating" (int): 4,
                }
                {
                    Todos los campos son requeridos menos el phone2

                    dependent_from: {
                        "first_name" (str): string,
                        "last_name" (str): string,
                        "email" (str): string,
                        "phone" (str): string,
                        "phone2" (str): string,
                    }
                }

                En caso de que el cliente no tenga dependiente, el segundo objeto debe ser:
                dependent_from: {
                    "same_as_client": True
                }
            }

        """
        
        # getting the data from the request that comes "separated"
        user:KumbioUser | KumbioToken = None

        if request.user == 'KUMBIO_TOKEN':
            user = request.auth
        else:
            user = request.user


        client_data:dict = request.data['client']
        dependent_from:dict = request.data['dependent_from']

        if isinstance(user, KumbioToken):
            client_data['created_by'] = user.app
        else:
            client_data['created_by'] = 3 # use enums here


        client_data['organization'] = user.organization.id

        client_serializer = OrganizationClientSerializer(data=client_data)
        
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status.HTTP_400_BAD_REQUEST)

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
        
        if not dependent_from_serializer.is_valid():
            return Response(dependent_from_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dependent_from_serializer.save()
        return Response(client_serializer.data, status.HTTP_201_CREATED)


# function types
@swagger_auto_schema(query_serializer=OrganizationClientTypeQuerySerializer(), method='GET')
@api_view(['GET'])
@authentication_classes([KumbioAuthentication])
@permission_classes([IsAuthenticated])
def get_organization_client_types(request):
    """
        Devuelve todos los tipos de cliente que una organización tiene asociados

        Obtener los campos extra dependiendo del tipo de cliente que se seleccione
        
        :Response 200:

            - fields: lista de campos extra, que se muestran como un array de arrays
            fields = [('name', TEXT), ('age', NUMBER)]

            donde el primer elemento es el nombre del campo y el segundo es el tipo de campo
    """

    user:KumbioUser | KumbioToken = None

    if isinstance(request.user, KumbioToken):
        user = request.auth
    else:
        user = request.user


    query_serializer = OrganizationClientTypeQuerySerializer(data=request.query_params)
    query_serializer.is_valid(raise_exception=True)
    query_params = query_serializer.data

    if query_params['client_type_id']:
        client_types = user.organization.client_types.filter(id=query_params['client_type_id'])

        if not client_types:
            raise exceptions.NotFound(_('el tipo de cliente no existe'))
    else:
        client_types = user.organization.client_types.all()

    client_types_serializer = OrganizationClientTypeSerializer(client_types, many=True)
    return Response(client_types_serializer.data, status=status.HTTP_200_OK)



@swagger_auto_schema(query_serializer=OrganizationClientTypeQuerySerializer(), method='GET')
@api_view(['GET'])
@authentication_classes([KumbioAuthentication])
@permission_classes([IsAuthenticated])
def get_extra_fields_for_client_type(request):
    """
        Obtener los campos extra dependiendo del tipo de cliente que se seleccione
        
        :Response 200:

            - fields: lista de campos extra, que se muestran como un array de arrays
            fields = [('name', TEXT), ('age', NUMBER)]

            donde el primer elemento es el nombre del campo y el segundo es el tipo de campo
    """

    user:KumbioUser | KumbioToken = None

    if isinstance(request.user, KumbioToken):
        user = request.auth
    else:
        user = request.user

    client_type_id = request.query_params.get('client_type_id', None)

    if not client_type_id:
        raise exceptions.ValidationError(_('client_type_id es requerido'))
    

    client_type = user.organization.client_types.filter(id=client_type_id)
    if not client_type:
        raise exceptions.NotFound(_('client type no se ha encontrado'))
    

    extra_fields = client_type[0].fields
    
    return Response(extra_fields, status=status.HTTP_200_OK)



@swagger_auto_schema(query_serializer=OrganizationClientTypeQuerySerializer(), method='GET')
@api_view(['GET'])
def create_clients(request):

    """
    
        Este endpoint es para crear clientes, se crean 10 clientes entrando en este endpoint
    
    """
    clients = []

    client_type:OrganizationClientType = OrganizationClientType.objects.get(id=18)

    for i in range(10):
        dependent_from = {
            'first_name': 'parent first name' + str(i),
            'last_name': 'parent last name' + str(i),
            'email': 'parent@email.com' + str(i),
            'phone': 'parent phone' + str(i),
        }

        client_data = {
            'organization': 'Yqe0DxtbwcK3KYrakqXY83brcZOr',
            'type': client_type.pk, # type must come from the organization sector type
            'first_name': 'child' + str(i),
            'last_name': 'child' + str(i),
            'email': 'client@email.com' + str(i),
            'phone': 'client phone' + str(i),
        }


        extra_fields:list[tuple] = client_type.fields
        converted_extra_fields:list[list] = []

        for index, field in enumerate(extra_fields):
            field = list(field)

            if field[1] == 'TEXT':
                field.append('value' + str(index))
            
            elif field[1] == 'NUMBER':
                num = int(f'{index}0{i}')
                field.append(num)

            converted_extra_fields.append(field)

        client_data['extra_fields'] = converted_extra_fields

        data_to_create_client = {
            'client': client_data,
            'dependent_from': dependent_from,
        }

        clients.append(data_to_create_client)


    data_from_serializer = list()

    for client in clients:
        client_serializer= OrganizationClientSerializer(data=client['client'])
        client_serializer.is_valid(raise_exception=True)
        client_serializer.save()

        client['dependent_from']['client'] = client_serializer.data['id']
        dependent_from_serializer = OrganizationClientDependentFromSerializer(data=client['dependent_from'])
        dependent_from_serializer.is_valid(raise_exception=True)
        dependent_from_serializer.save()

        client_instance:OrganizationClient = client_serializer.instance
        client_serializer = OrganizationClientSerializer(client_instance)

        data_from_serializer.append(client_serializer.data)

    return Response(data_from_serializer, status=status.HTTP_201_CREATED)