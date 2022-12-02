from django.shortcuts import render

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AppointmentInvoiceSerializer

# Create your views here.

class AppointmentInvoiceViewSet(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) # Use this token?


    def get(self, request):
        pass


    def post(self, request):
        pass

