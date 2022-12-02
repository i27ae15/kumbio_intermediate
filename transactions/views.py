from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .query_serializers import AppointmentInvoiceQuerySerializer
from .serializers import AppointmentInvoiceSerializer

from print_pp.logging import Print
# Create your views here.

class AppointmentInvoiceViewSet(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) # Use this token?


    def get(self, request):
        
        query_serializer = AppointmentInvoiceQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True, context={'organization_id': request.user.organization.id})
        query_params = query_serializer.validated_data

    
    @swagger_auto_schema(request_body=AppointmentInvoiceSerializer())
    def post(self, request):

        request.data['created_by'] = request.user.id
        
        serializer = AppointmentInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

