# python 
# django
from django.urls import reverse

from rest_framework.test import APITestCase
from organization_info.tests import create_organization, create_place, create_user, create_kumbio_role, create_service
from organization_info.serializers import OrganizationPlaceSerializer, OrganizationServiceSerializer

# models
from user_info.models import KumbioUser, KumbioUserRole

# serializers

from print_pp.logging import Print


class TestGetAvailablePlacesForUser(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.kumbio_role = create_kumbio_role()
        self.user = create_user(self.organization, self.kumbio_role)

        self.data_to_create_place = {
            "organization" : self.organization.id,
            "address": "la calle de al lado",
            "name": "Dresden",
            "created_by": self.user.pk
        }

    def test_get_available_places_for_user(self):

        self.place = create_place(self.data_to_create_place, self.organization, self.user)
        self.user.available_places.add(self.place)

        url = reverse('user_info:get_available_places_for_user')
        data = {'user_id': self.user.pk}
        response = self.client.get(url, data, format='json').json()

        Print(response)
        

class TestGetAvailableSerivicesForUser(APITestCase):
    
    def setUp(self) -> None:
        self.organization = create_organization()
        self.kumbio_role = create_kumbio_role()
        self.data_to_create_service = {
            "organization" : self.organization.id,
            "service": "testing service",
            "description": "testing description",
            "price": 100
        }
        self.url = reverse('user_info:get_available_services_for_user')
        
    
    def test_get_available_services_for_user(self):
        
        first_user = create_user(self.organization, self.kumbio_role)
        service = create_service(self.data_to_create_service, self.organization)
        first_user.available_services.add(service)
        data = {'user_id': first_user.pk}
        
        response = self.client.get(self.url, data, format='json').json()
        
        service_data = dict(available_services=[OrganizationServiceSerializer(service).data])
        self.assertEqual(response, service_data)    
        
        second_user = create_user(self.organization, self.kumbio_role, username='second_user', email='second_user@email.com')
        data = {'user_id': second_user.pk}
        
        response = self.client.get(self.url, data, format='json').json()
        
        self.assertEqual(response, dict(available_services=[]))
        
        