# python
import requests
import os


# django
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

# query serializers
from .serializers.query_serializers import (OrganizationPlaceQuerySerializer, OrganizationProfessionalQuerySerializer,
OrganizationSectorQuerySerializer, OrganizationServiceQuerySerializer, OrganizationClientQuerySerializer,
OrganizationClientTypeQuerySerializer, OrganizationQuerySerializer)

# body serializers
from .serializers.body_serializers import (PlacePutSerializer, OrganizationClientPutSerializer, 
OrganizationProfessionalPostBodySerializer, OrganizationProfessionalPutBodySerializer,
OrganizationPlacePostSerializer, OrganizationClientDeleteSerializer)



# model serializers
from .serializers.model_serializers import (OrganizationProfessionalSerializer, OrganizationPlaceSerializer, OrganizationSerializer, OrganizationSectorSerializer, 
OrganizationServiceSerializer, DayAvailableForPlaceSerializer, OrganizationClientSerializer, OrganizationClientDependentFromSerializer,
OrganizationClientTypeSerializer, DayAvailableForProfessionalSerializer)


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
        operation_description="Obtener el objecto de la organización del usuario",
        query_serializer=OrganizationQuerySerializer,
        responses={
            200: openapi.Response(
                description="Organization",
                schema=OrganizationSerializer
            )
        }
    )
    def get(self, request):
        query_serializer = OrganizationQuerySerializer(data=request.GET)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        organization_id = query_params.get('organization_id')

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
        serializer = OrganizationSerializer(organization, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class OrganizationProfessionalView(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)


    @swagger_auto_schema(
    operation_description="Obtener todos los profesionales de la organización",
    query_serializer=OrganizationProfessionalQuerySerializer,
    responses={
        200: openapi.Response(
            description="Profesionales de la organización",
            schema=OrganizationProfessionalSerializer(many=True)
        ),
        401: openapi.Response(
            description="No autorizado",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    })
    def get(self, request):
        """
            Get all the professionals of the organization
        """

        query_serializer = OrganizationProfessionalQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        organization_professionals:QuerySet[OrganizationProfessional] = None

        if query_params['kumbio_user_id']:
            organization_professionals = OrganizationProfessional.objects.filter(kumbio_user__id=int(query_params['kumbio_user_id']))
        else:
            organization_professionals = OrganizationProfessional.objects.filter(organization__id=query_params['organization_id'])
        serializer = OrganizationProfessionalSerializer(organization_professionals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



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
                    raise exceptions.PermissionDenied(_("You are not authorized to perform this action"))
                    
            organization_professionals = OrganizationProfessional.objects.filter(kumbio_user__id=int(query_params['kumbio_user_id']))

        serializer = OrganizationProfessionalSerializer(organization_professionals, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
    operation_description="Crear un nuevo profesional de la organización",
    request_body=OrganizationProfessionalPostBodySerializer,
    responses={
        201: openapi.Response(
            description="Profesional de la organización creado",
            schema=OrganizationProfessionalSerializer
        ),
        400: openapi.Response(
            description="Error de validación",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    })
    def post(self, request):
        """
        Crea un nuevo profesional en la organización.

        Body Parameters:
        - email (str): Correo electrónico del profesional.
        - first_name (str): Nombre del profesional.
        - last_name (str): Apellido del profesional.
        - phone (str): Teléfono del profesional.
        - username (str): Nombre de usuario del profesional.
        - organization (int): ID de la organización del profesional.
        - password (str): Contraseña del profesional.
        """
        
        # OrganizationProfessional hereda de KumbioUser, por lo que para crear un nuevo profesional primero hay que crear 
        # un usuario Kumbio

        body_serializer = OrganizationProfessionalPostBodySerializer(data=request.data)
        body_serializer.is_valid(raise_exception=True)
        body_data:dict = body_serializer.validated_data
        
        # Se crea el usuario Kumbio
        kumbio_user_serializer = CreateKumbioUserSerializer(body_data, context={'set_verified_email': True})
        kumbio_user_serializer.is_valid(raise_exception=True)

        # Se obtiene el token del usuario creado en el calendario
        token = self.__create_calendar_user(body_data)
        
        # Se guarda el usuario Kumbio
        kumbio_user_serializer.save()
        kumbio_user:KumbioUser = kumbio_user_serializer.instance
        
        # Se guarda la información extra del usuario y se serializa el profesional
        professional_data = self.__save_user_extra_information(kumbio_user, body_data, calendar_token=token, created_by=request.user.id)
        professional_serializer = OrganizationProfessionalSerializer(data=professional_data)
        professional_serializer.is_valid(raise_exception=True)
        professional_serializer.save()
                
        return Response(professional_serializer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
    operation_description="Actualizar un profesional",
    request_body=OrganizationProfessionalPutBodySerializer,
    responses={
        200: openapi.Response(
            description="Profesional actualizado",
            schema=OrganizationProfessionalSerializer
        ),
        400: openapi.Response(
            description="Error de validación",
        )
    })
    def put(self, request):
        """
        Parameters:
        - professional_id (int): id of the professional to update
        - professional_data (dict): data to update the professional with
        - days (list): list of days to update the professional with = [
            {
                week_day: (int) day of the week
                exclude:list = [[0, 7], [18, 23]]
            }
        ]
        """

        body_serializer = OrganizationProfessionalPutBodySerializer(data=request.data)
        body_serializer.is_valid(raise_exception=True)
        body_data:dict = body_serializer.validated_data
        
        professional:OrganizationProfessional = body_data['professional']

        professional_serializer = OrganizationProfessionalSerializer(professional, data=body_data['professional_data'], partial=True)
        professional_serializer.is_valid(raise_exception=True)
        professional_serializer.save()

        professional_object:OrganizationProfessional = professional_serializer.instance
        
        services = body_data['professional_data'].get('services_ids', [])
        
        professional_object.services.clear()
        for service_id in services:
            professional_object.services.add(service_id)

        specialties = body_data['professional_data'].get('specialties_ids', [])

        professional_object.specialties.clear()
        for specialty_id in specialties:
            professional_object.specialties.add(specialty_id)

        if days:= body_data.get('days'):
            for day in days:

                available_day = professional_object.get_day_available(day['week_day'])
                day_serializer = None

                if available_day:
                    day_serializer = DayAvailableForProfessionalSerializer(available_day, data=day, partial=True)
                    day_serializer.is_valid(raise_exception=True)
                    day_serializer.save()
                else:
                    # this will mean that this day has not been created yet, so we have to create it
                    day['professional'] = professional_object.id
                    day_serializer = DayAvailableForProfessionalSerializer(data=day)
                    day_serializer.is_valid(raise_exception=True)
                    day_serializer.save()
        

        return Response(professional_serializer.data, status=status.HTTP_200_OK)
    

    # Private functions
    def __create_calendar_user(self, request_data:dict) -> str:
        
        """
            Crea un nuevo usuario en el calendario.

            Parameters:
            - organization_id (int): ID de la organización.
            - email (str): Correo electrónico del usuario.
            - first_name (str): Nombre del usuario.
            - last_name (str): Apellido del usuario.

            Returns:
            - str: Token del usuario creado en el calendario.
        """

        # TODO: manejar la eliminación del usuario creado en caso de que no se haya creado correctamente
        
        res = requests.post(f'{CALENDAR_ENDPOINT}register/api/v2/create-user/', 
        json={
            'organization_id': request_data['organization_id'],
            'email':request_data['email'],
            'first_name': request_data['first_name'],
            'last_name': request_data['last_name'],
            'role': PROFESSIONAL_ROLE_ID, 
        })
        
        # Si la respuesta no tiene un código de estado HTTP 201 o no incluye el token, se lanza una excepción
        if res.status_code != status.HTTP_201_CREATED or 'token' not in res.json():
            try:
                raise exceptions.APIException(_(res.json()))
            except Exception as e:
                raise exceptions.APIException(_("Something went wrong with the calendar_api: {e}"))
        
        # Si la respuesta tiene un código de estado HTTP
        return res.json()['token']


    def __save_user_extra_information(self, kumbio_user:KumbioUser, request_data:dict, calendar_token:dict, created_by:int) -> dict:
        """
        Guarda la información extra del usuario.

        Parameters:
        - kumbio_user (KumbioUser): Instancia del usuario.
        - request_data (dict): Datos de la petición.
        - calendar_token (str): Token del usuario creado en el calendario.
        - created_by (int): ID del usuario que creó al profesional.

        Returns:
        - dict: Datos del profesional.
        """

        # Asigna el rol de "organization_professional" al usuario y guarda la organización y el token del calendario
        kumbio_user.role = KumbioUserRole.objects.get(id=PROFESSIONAL_ROLE_ID)
        kumbio_user.organization = Organization.objects.get(id=request_data['organization_id'])
        kumbio_user.calendar_token = calendar_token
        kumbio_user.set_password(request_data['password'])
        kumbio_user.save()

        # Crea una copia de los datos de la petición y agrega el ID del usuario que creó al profesional y el ID del usuario Kumbio
        professional_data = request_data.copy()
        professional_data['created_by_id'] = created_by
        professional_data['kumbio_user_id'] = kumbio_user.pk

        return professional_data


class OrganizationPlaceView(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 


    @swagger_auto_schema(
    operation_description="Obtener lugares de la organización del usuario",
    query_serializer=OrganizationPlaceQuerySerializer,
    responses={
        200: openapi.Response(
            description="Lugares de la organización",
            schema=OrganizationPlaceSerializer
        )
    })
    def get(self, request):
        """
            Get places 
        """

        query_serializer = OrganizationPlaceQuerySerializer(data=request.query_params, context = {'organization': request.user.organization})
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        places = query_params['places']
            
        place_serializer = OrganizationPlaceSerializer(places, many=True)
        
        return Response(place_serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
    request_body=OrganizationPlacePostSerializer,
    responses={
        201: openapi.Response(
            description="Datos del lugar creado",
            schema=OrganizationPlaceSerializer
        ),
        400: openapi.Response(
            description="Error de validación",
        )
    })
    @check_if_user_is_admin_decorator
    def post(self, request):
        """
            Create a new Place
            Solo los administradores pueden crear lugares

            para esto es necesario pasar dos objectos uno de place, 
            para crear el lugar y otro para los días que ese lugar acepta, 
            iniciando con Monday = 0


            request body:

                # if this place has a custom price for a service
                la propiedad custom_price se tiene esta estructura
                    custom_price:list[dict] = [{
                        place_id: 1,
                        price: 25,
                    }]
        """

        body_serializer = OrganizationPlacePostSerializer(
            data=request.data, 
            context={'organization': request.user.organization.id, 'created_by': request.user.id}
        )
        body_serializer.is_valid(raise_exception=True)
        body_data:dict = body_serializer.validated_data

        place_serializer = OrganizationPlaceSerializer(data=body_data['place'])
    
        if place_serializer.is_valid():
            place_serializer.save()

            daysAvailable:list[dict] = body_data['days']

            if daysAvailable:
                for day in daysAvailable:
                    day['place'] = place_serializer.data['id']

                days_available_serializer = DayAvailableForPlaceSerializer(data=daysAvailable, many=True)

                days_available_serializer.is_valid(raise_exception=True)
                days_available_serializer.save()
            

            place_serializer = OrganizationPlaceSerializer(place_serializer.instance)

            return Response(place_serializer.data, status.HTTP_201_CREATED)
        
        return Response(place_serializer.errors, status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
    request_body=PlacePutSerializer,
    responses={
        200: openapi.Response(
            description="Datos del lugar actualizados",
            schema=OrganizationPlaceSerializer
        ),
        400: openapi.Response(
            description="Error de validación",
        )
    })
    @check_if_user_is_admin_decorator
    def put(self, request):
        """

            Si se quiere añadir otro dia al lugar, se hace desde aquí, añadiendo el dia a la lista de 
            días disponibles

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
        # TODO: when a schedule for a place is modified, this must modified also the schedule of 
        # the professionals that work in that place
        
        body_serializer = PlacePutSerializer(data=request.data, context={'organization': request.user.organization})
        body_serializer.is_valid(raise_exception=True)
        body_data = body_serializer.validated_data

        place_serializer = OrganizationPlaceSerializer(body_data['place'], data=body_data['place_data'], partial=True)
        place_serializer.is_valid(raise_exception=True)
        place_serializer.save()
        place_object:OrganizationPlace = place_serializer.instance

        data_to_return = dict(place=place_serializer.data, days=list())
        
        if days := body_data['days_data']:
            data_to_return['days'] = self.__update_and_create_days(days, place_object)
        
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
            place:OrganizationPlace = OrganizationPlace.objects.get(id=request.data['place_id'], organization=request.user.organization)
        except KeyError:
            raise exceptions.NotFound(_('No se ha encontrado el lugar'))

        place.delete()
        # TODO: Perform communication with calendar api to delete calendars

        return Response({'message': 'lugar eliminado'}, status=status.HTTP_200_OK)
    

    def __update_and_create_days(self, days:list, place:OrganizationPlace) -> list[dict]:
        data_to_return = list()
        for day in days:

            available_day = place.get_day_available(day['week_day'])
            day_serializer = None

            if available_day:
                day_serializer = DayAvailableForPlaceSerializer(available_day, data=day, partial=True)
            else:
                # this will mean that this day has not been created yet, so we have to create it
                day_serializer = DayAvailableForPlaceSerializer(data=day)
            
            day_serializer.is_valid(raise_exception=True)
            day_serializer.save()
            
            data_to_return.append(day_serializer.data)
        
        return data_to_return


class OrganizationSectorView(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 

    
    @swagger_auto_schema(
        query_serializer=OrganizationSectorQuerySerializer(),
    )
    def get(self, request):

        query_serializer = OrganizationSectorQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data
        
        if query_params['sector_id']:
            sectors = Sector.objects.filter(id=query_params['sector_id'])
            if not sectors:
                raise exceptions.NotFound(_('el sector no existe'))
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
    
            query_serializer = OrganizationServiceQuerySerializer(data=request.query_params)
            query_serializer.is_valid(raise_exception=True)
            query_params = query_serializer.validated_data
            
            if query_params['service_id']:
                services = OrganizationService.objects.filter(id=query_params['service_id'])
                if not services:
                    raise exceptions.NotFound(_('el servicio no existe'))
            
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
        
            service_serializer.is_valid(raise_exception=True)
            service_serializer.save()
    
            return Response(service_serializer.data, status.HTTP_201_CREATED)
            

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

        if not isinstance(request.user, KumbioToken):
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
            
            clients = clients.filter(age__gte=query_params['min_age'],
                           age__lte=query_params['max_age'],
                           rating__gte=query_params['min_rating'],
                           rating__lte=query_params['max_rating'])

            if query_params['birth_date']:
                clients = clients.filter(birth_date=query_params['birth_date'])

        client_serializer = OrganizationClientSerializer(clients, many=True)
        return Response(client_serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema()
    def post(self, request):

        """
        
        La información para crear un nuevo cliente debe enviarse en dos objetos JSON en la solicitud. 

        El primero debe contener los datos del cliente, mientras que el segundo debe contener los datos
        del dependiente del cliente. Si el cliente no tiene un dependiente, el segundo objeto debe tener 
        una propiedad llamada "same_as_client" con el valor "True".

        Los campos necesarios para completar el objeto "extra_fields" se pueden obtener de la ruta 
        "organization/client_types/".

        Ejemplo de cuerpo de la solicitud:


        {
            "client": {
                "type": client_type_id (int, requerido),
                "first_name": "nombre" (str, requerido),
                "last_name": "apellido" (str, requerido),
                "extra_fields": [
                    ("pets_first_name", FieldType.TEXT, "Juan Carlos"), 
                    ("pets_last_name", FieldType.TEXT, "Atrida")
                ],
                "birthday": "YYYY-MM-DD" (str), 
                "comments": "comentarios" (str),
                "identification": "identificación" (str),
                "age": 25 (int),
                "rating": 4 (int),
            }
        }
        {
            "client": client_data,
            "dependent_from": {
                "first_name": string (str, requerido),
                "last_name": string (str, requerido),
                "email": string (str, requerido),
                "phone": string (str, requerido),
                "phone2": string (str)
            }
        }

        En caso de que el cliente no tenga un dependiente, el segundo objeto debe ser:

        {
            "client": client_data,
            "dependent_from": {
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


    @swagger_auto_schema(request_body=OrganizationClientPutSerializer())
    def put(self, request):

        """
            body parameters:
            client_id (int) (required): id del cliente
            client_data (dict) (required): {}
        """

        # write a similar as above, for the client put
        try:
            client = OrganizationClient.objects.get(id=request.data['client_id'])
        except OrganizationClient.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        client_serializer = OrganizationClientSerializer(client, data=request.data['client_data'], partial=True)
        client_serializer.is_valid(raise_exception=True)
        client_serializer.save()

        return Response(client_serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=OrganizationClientDeleteSerializer())
    def delete(self, request):

        """
            body parameters:
            client_id (int) (required): id del cliente
        """

        try:
            client = OrganizationClient.objects.get(id=request.data['client_id'])
        except OrganizationClient.DoesNotExist:
            raise exceptions.NotFound(_("Client not found"))

        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
    query_params = query_serializer.validated_data

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
        string_i = str(i)
        dependent_from = {
            'first_name': 'parent first name' + string_i,
            'last_name': 'parent last name' + string_i,
            'email': 'parent@email.com' + string_i,
            'phone': 'parent phone' + string_i,
        }

        client_data = {
            'organization': 'Yqe0DxtbwcK3KYrakqXY83brcZOr',
            'type': client_type.pk, # type must come from the organization sector type
            'first_name': 'child' + string_i,
            'last_name': 'child' + string_i,
            'email': 'client@email.com' + string_i,
            'phone': 'client phone' + string_i,
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