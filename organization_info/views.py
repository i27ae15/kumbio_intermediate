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
from .models.main_models import Organization, OrganizationProfessional, OrganizationPlace

# serializers
from user_info.serializers import KumbioUserSerializer, CreateKumbioUserSerializer

from .query_serializers import PlaceQuerySerializer
from .serializers import OrganizationProfessionalSerializer, OrganizationPlaceSerializer

# others
from print_pp.logging import Print

# Functions

def check_if_user_is_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.role.name == 'ORGANIZATION ADMIN':
            return func(self, request, *args, **kwargs)
        else:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


# classes


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

        qp = PlaceQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        qp = qp.data

        if qp['place_id']:
            places = self.check_if_place_exists(request.user, int(qp['place_id']))

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
    @check_if_user_is_admin
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
    @check_if_user_is_admin
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
    @check_if_user_is_admin
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




    # def add_default_templates_to_calendar(self, user_id:int, def_start:int, data:dict) -> dict:

    #     templates = self.check_if_templates_exist(user_id, def_start)

    #     data['template_to_send_as_confirmation'] = templates[0]
    #     data['template_to_send_as_reminder_1'] = templates[1]
    #     data['template_to_send_as_reminder_2'] = templates[1]
    #     data['template_to_send_as_reminder_3'] = templates[1]
    #     data['template_to_send_as_rescheduled'] = templates[2]
    #     data['template_to_send_as_canceled'] = templates[3]
    #     data['template_to_send_as_new_client_to_calendar_user'] = templates[4]
    #     data['template_to_send_as_rescheduled_to_calendar_user'] = templates[5]
    #     data['template_to_send_as_canceled_to_calendar_user'] = templates[6]
    
    # def check_if_templates_exist(slef, user_id:int, def_start:int) -> list:
    #     templates = []
    #     for i in range(def_start, def_start + 7):
    #         try:
    #             'MailTemplate'.objects.get(id=i, user=user_id)
    #             templates.append(i)
    #         except 'MailTemplate'.DoesNotExist:
    #             templates.append(None)
        
    #     return templates
