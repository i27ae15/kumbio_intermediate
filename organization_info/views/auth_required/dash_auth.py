from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated


# authentication
from authentication_manager.authenticate import ClientDashboardAuthentication

# serializers
# query serializers
from organization_info.serializers.query_serializers import (
    OrganizationPlaceDashboardInfoQuerySerializer, OrganizationProfessionalQuerySerializer, 
    OrganizationServiceDashboardInfoQuerySerializer, OrganizationQuerySerializer
)

#  organization dashboard serializers
from organization_info.serializers.dashboard_info_serializer import (
    OrganizationDashboardInfoSerializer, OrganizationServiceDashboardInfoSerializer,
    OrganizationProfessionalDashboardInfoSerializer, OrganizationPlaceDashboardInfoSerializer
)


#swagger
from drf_yasg.utils import swagger_auto_schema


class OrganizationDashboardInfoView(APIView):

    # Using the class here cause for some reason the decorators does not take the authentication_classes and permission_classes

    permission_classes = (IsAuthenticated,)
    authentication_classes = (ClientDashboardAuthentication,)

    @swagger_auto_schema(query_serializer=OrganizationQuerySerializer(), tags=['booking_dashboard'])
    def get(self, request):
        query_serializer = OrganizationQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data
        
        organization = query_params['organization']

        organization_serializer = OrganizationDashboardInfoSerializer(organization)
        return Response(organization_serializer.data, status=status.HTTP_200_OK)


class OrganizationServiceDashboardInfoView(APIView):

    # Using the class here cause for some reason the decorators does not take the authentication_classes and permission_classes

    permission_classes = (IsAuthenticated,)
    authentication_classes = (ClientDashboardAuthentication,)

    @swagger_auto_schema(query_serializer=OrganizationServiceDashboardInfoQuerySerializer(), tags=['booking_dashboard'])
    def get(self, request):
        query_serializer = OrganizationServiceDashboardInfoQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        service = query_params['service']

        service_serializer = OrganizationServiceDashboardInfoSerializer(service)
        return Response(service_serializer.data, status=status.HTTP_200_OK)


class OrganizationProfessionalDashboardInfoView(APIView):

    # Using the class here cause for some reason the decorators does not take the authentication_classes and permission_classes

    permission_classes = (IsAuthenticated,)
    authentication_classes = (ClientDashboardAuthentication,)


    @swagger_auto_schema(query_serializer=OrganizationProfessionalQuerySerializer(), tags=['booking_dashboard'])
    def get(self, request):
        query_serializer = OrganizationProfessionalQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        professionals = query_params['professionals']

        professional_serializer = OrganizationProfessionalDashboardInfoSerializer(professionals, many=True)
        return Response(professional_serializer.data, status=status.HTTP_200_OK)


class OrganizationPlaceDashboardInfoView(APIView):

    # Using the class here cause for some reason the decorators does not take the authentication_classes and permission_classes

    permission_classes = (IsAuthenticated,)
    authentication_classes = (ClientDashboardAuthentication,)

    @swagger_auto_schema(query_serializer=OrganizationPlaceDashboardInfoQuerySerializer(), tags=['booking_dashboard'])
    def get(self, request):
        query_serializer = OrganizationPlaceDashboardInfoQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.validated_data

        place = query_params['place']

        place_serializer = OrganizationPlaceDashboardInfoSerializer(place)
        return Response(place_serializer.data, status=status.HTTP_200_OK)
