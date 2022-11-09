# python 
# django
from django.urls import reverse
from .models.main_models import Organization, OrganizationPlace

from rest_framework.test import APITestCase

# models
from user_info.models import KumbioUser, KumbioUserRole

# serializers 
from .serializers import OrganizationPlaceSerializer

from print_pp.logging import Print


EMAIL='testuser@testuser.com'
PASSWORD = 'testuser'
USERNAME = 'testuser'


def create_kumbio_role() -> KumbioUserRole:
    return KumbioUserRole.objects.create(
        name='ORGANIZATION ADMIN',
        description='ORGANIZATION ADMIN')
   
   
def create_user(organization:Organization, role:KumbioUserRole) -> KumbioUser:
    return KumbioUser.objects.create_user(
        username=USERNAME,
        email=EMAIL,
        first_name='test',
        last_name='user',
        password=PASSWORD,
        organization=organization,
        is_email_verified=True,
        role=role)
    

def create_organization(use_user=False) -> Organization:
    
    org = Organization.objects.create(
        name='test organization',
        description='test organization description',
        email='organization@email.com',
        phone='132456789',
        owner_email='organizariononwer@email.com',
        owner_first_name='test',
        owner_last_name='organization',
        owner_phone='123456789')

    if use_user:
        role = create_kumbio_role()
        user = create_user(org, role)
        org.owner_email = user.email
        org.save()
    
    return org


class TestOrganizationCreation(APITestCase):
    
    def test_organization_creation(self):
        organization = create_organization(use_user=True)
        Print((
            'organization information',
            organization.email_templates, 
            organization.name,
            organization.description, 
            organization.phone,
            organization.owner_email,
            organization.owner_first_name,
            organization.owner_last_name,
            organization.owner_phone,
        ))


class TestPlace(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.user = create_user(self.organization, create_kumbio_role())
        self.set_authorization()
        
        self.data_to_create_place = {
            "organization" : self.organization.id,
            "address": "la calle de al lado",
            "name": "Dresden",
            "created_by": self.user.id
        }
        self.place = self.create_place(self.organization, self.user)
        
        Print('Testing setup for TestPlace completed')

    
    def test_place_creation(self):

        self.assertTrue(self.client.login(email=EMAIL, password=PASSWORD))

        initial_data = self.create_place(self.organization, self.user, create_with_serializer=True)
        
        del initial_data['datetime_created']
        del initial_data['id']

        url = reverse('organization_info:place')
        response = self.client.post(url, self.data_to_create_place, format='json').json()
        
        try:
            del response['datetime_created']
            del response['id']
        except KeyError:
            self.assertEqual('youre not authorized', '')
            

        Print('New place created', response)

        self.assertEqual(response, initial_data)


    # helper functoins ---------------------------------------------------------

    def create_place(self, organization:Organization, user:KumbioUser, create_with_serializer=False, data_to_create_place=None) -> OrganizationPlace:
        # create a post

        if data_to_create_place is None:
            data_to_create_place = self.data_to_create_place


        if not create_with_serializer:
            return OrganizationPlace.objects.create(
                organization=organization,
                created_by=user,
                address='testing address',
                name='testing name')


        serializer = OrganizationPlaceSerializer(data=data_to_create_place)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        initial_data = serializer.data

        return initial_data

    
    def set_authorization(self):
        url = reverse('register:obtain_auth_token')
        # TODO: Check why we have to passs the email as username
        resp = self.client.post(url, {'username':EMAIL, 'password':PASSWORD, 'for_kumbio': True}, format='json')
        
        Print('Response from auth', resp.json())
    
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)