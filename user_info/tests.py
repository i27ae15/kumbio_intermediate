# python 
# django
from django.urls import reverse

from rest_framework.test import APITestCase
from organization_info.tests import create_organization, create_place, create_user, create_kumbio_role

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
        data = {'user_id': self.user.id}
        response = self.client.get(url, data, format='json').json()

        Print(response)
        
