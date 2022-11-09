# python 
# django
from django.urls import reverse

from rest_framework.test import APITestCase

# models
from user_info.models import KumbioUser, KumbioUserRole

# serializers

from print_pp.logging import Print


class TestCreateUser(APITestCase):

    def setUp(self) -> None:        
        self.data_to_create_user = {
            "email": "andresruse18@gmail.com",
            "password": "password123",
            "username": "user_number1",
            "first_name": "calendar_first_name1",
            "last_name": "calendar_second_name1",
            "phone": "123465798",
            "organization": {
                "name": "organization_name",
                "email": "andresruse18@email.com",
                "phone": "organization_phone"
            }
        }
        
        Print('Testing setup for CreateUser completed')

    
    def test_user_creation(self):

        url = reverse('register:create_user')
        response = self.client.post(url, self.data_to_create_user, format='json').json()
        
        Print(response)