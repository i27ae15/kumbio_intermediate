from django.utils.translation import gettext_lazy as _


from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


from drf_yasg.utils import swagger_auto_schema
from drf_yasg.codecs import openapi


# models
from organization_info.models import Organization, ClientParent, OrganizationClient
from organization_info.models.main_models import OrganizationService


# serializers
from organization_info.serializers.body_serializers import (
    OrganizationClientForCalendarBodySerializer, IncrementNumberOfAppointmentsBodySerializer
)
from organization_info.serializers.model_serializers import (
    ClientParentSerializer, OrganizationClientSerializer, 
    OrganizationClientRelatedFieldsSerializer,
)


from print_pp.logging import Print


class ClientForCalendar(APIView):

    @swagger_auto_schema(tags=['client'])
    def get(self, request):

        """
            This get if for getting the parent of a client
        """

        parent_client_email:int = request.query_params.get('parent_client_email', None)
        parent_client_id:int = request.query_params.get('parent_client_id', None)
        
        if not parent_client_email and not parent_client_id: 
            raise exceptions.ValidationError(_('parent_client_email or parent_client_id is required'))

        client:ClientParent
        if parent_client_email:
            try: client = ClientParent.objects.get(email=parent_client_email)
            except ClientParent.DoesNotExist: raise exceptions.NotFound(_('client_parent not found'))
        else:
            try: client = ClientParent.objects.get(id=parent_client_id)
            except ClientParent.DoesNotExist: raise exceptions.NotFound(_('client_parent not found'))
        

        client_parent_serializer = ClientParentSerializer(client)
        
        return Response(client_parent_serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=OrganizationClientForCalendarBodySerializer, tags=['client'])
    def post(self, request):

        """
            This method will be only available for creating new users from the calendar endpoint
        """
        
        body_serializer = OrganizationClientForCalendarBodySerializer(data=request.data)
        body_serializer.is_valid(raise_exception=True)
        body_data = body_serializer.validated_data

        organization:Organization = body_data['organization']

        data_to_serialize = body_data['client_parent']
        data_to_serialize['organization'] = organization.pk

        client_parent_serializer = ClientParentSerializer(data=body_data['client_parent'])
        client_parent_serializer.is_valid(raise_exception=True)
        client_parent_serializer.save()
        parent:ClientParent = client_parent_serializer.instance
        
        client_type = organization.client_types[0]
        extra_fields = list()
        value = ''
        
        for field in client_type.fields:
            if field[1] != 'TEXT':
                value = 0
            else:
                value = ''
            
            extra_fields.append([field[0], field[1], value])

        new_client_data = {
            'client_parent': parent.pk,
            'type': client_type.pk,
            'extra_fields': extra_fields,
        }

        if parent.same_as_client:
            new_client_data['first_name'] = parent.first_name
            new_client_data['last_name'] = parent.last_name
        else:
            new_client_data['first_name'] = body_data['client']['first_name']
            new_client_data['last_name'] = body_data['client']['last_name']


        new_client = OrganizationClientSerializer(data=new_client_data)
        new_client.is_valid(raise_exception=True)
        new_client.save()


        parent.refresh_from_db()
        data_to_return = ClientParentSerializer(parent).data

        return Response(data_to_return, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='get', tags=['client'])
@api_view(['GET'])
def get_client_for_calendar(request):

    client_id = request.GET.get('client_id', None)
    
    if not client_id: raise exceptions.ValidationError(_('client_id is required'))
    
    try: client = OrganizationClient.objects.get(id=client_id)
    except OrganizationClient.DoesNotExist: raise exceptions.NotFound(_('client not found'))

    client_serializer = OrganizationClientRelatedFieldsSerializer(client)
    return Response(client_serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', tags=['organization'], request_body=IncrementNumberOfAppointmentsBodySerializer)
@api_view(['POST'])
def increment_number_of_appointments(request):


    body_serializer = IncrementNumberOfAppointmentsBodySerializer(data=request.data)
    body_serializer.is_valid(raise_exception=True)
    body_data = body_serializer.validated_data
    
    organization:Organization = body_data['organization']
    service:OrganizationService = body_data['service']

    organization.increment_number_of_active_appointments()
    service.increment_number_of_active_appointments()

    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='get', 
    tags=['for_calendar'],
    manual_parameters=[
        openapi.Parameter(
            name='service_id',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True,
            description='service id',
        ),
    ],
    responses={
        200: openapi.Response(
            description='service name',
            examples={
                'application/json': {
                    'service_name': 'service name'
                }
            },
        ),
    },
)
@api_view(['GET'])
def get_service_name(request):

    service_id = request.GET.get('service_id', None)
    
    if not service_id: raise exceptions.ValidationError(_('service_id is required'))
    
    try: service:OrganizationService = OrganizationService.objects.get(id=service_id)
    except OrganizationService.DoesNotExist: raise exceptions.NotFound(_('service not found'))

    return Response({'service_name': service.service}, status=status.HTTP_200_OK)