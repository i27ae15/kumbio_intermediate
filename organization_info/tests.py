# python 
# django
from django.urls import reverse
from .models.main_models import (Organization, OrganizationPlace, OrganizationService, Sector, OrganizationClient, 
                                 OrganizationClientType, OrganizationProfessional)

from rest_framework.test import APITestCase

# models
from user_info.models import KumbioUser, KumbioUserRole
from .models.default_values import DEFAULT_CLIENT_TYPES

# serializers 
from .serializers import OrganizationPlaceSerializer, OrganizationServiceSerializer, OrganizationSectorSerializer
from authentication_manager.models import KumbioToken, AppToken

# utils
from organization_info.utils.enums import FieldType

from print_pp.logging import Print


EMAIL='testuser@testuser.com'
PASSWORD = 'testuser'
USERNAME = 'testuser'


def set_authorization(self, client):
    url = reverse('register:obtain_auth_token')
    # TODO: Check why we have to pass the email as username
    resp = client.post(url, {'username':EMAIL, 'password':PASSWORD, 'for_kumbio': True}, format='json')

    # check if token in resp.data
    if 'token' not in resp.data:
        Print(resp.json())
        raise Exception('Token not in resp.data')

    token = resp.data['token']

    client.credentials(HTTP_AUTHORIZATION='Token ' + token)


def create_organization_sector(data:dict=None) -> Sector:

    if not data:
        return Sector.objects.create(
            name='testing sector',
            description='testing sector description')
    
    return Sector.objects.create(**data)


def create_kumbio_role() -> KumbioUserRole:
    return KumbioUserRole.objects.create(
        name='ORGANIZATION ADMIN',
        description='ORGANIZATION ADMIN')
   
   
def create_user(organization:Organization, role:KumbioUserRole=None, username=USERNAME, email=EMAIL) -> KumbioUser:
    return KumbioUser.objects.create_user(
        username=username,
        email=email,
        first_name='test',
        last_name='user',
        password=PASSWORD,
        organization=organization,
        is_email_verified=True,
        role=role if role else create_kumbio_role())
    

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
        user = create_user(org)
        org.owner_email = user.email
        org.save()
    
    return org


def create_place(data_to_create_place:dict, organization:Organization, user:KumbioUser, create_with_serializer=False) -> OrganizationPlace:
    # create a post

    if not create_with_serializer:
        return OrganizationPlace.objects.create(
            organization=organization,
            created_by=user,
            address='testing address',
            name='testing name')

    serializer = OrganizationPlaceSerializer(data=data_to_create_place['place'])
    serializer.is_valid(raise_exception=True)
    serializer.save()
    initial_data = serializer.data

    return initial_data


def create_service(data_to_create_service:dict, organization:Organization, create_with_serializer=False) -> OrganizationService:
    # create a post
    
    if not create_with_serializer:
        return OrganizationService.objects.create(
            organization=organization,
            service='testing service',
            description='testing description',
            price=100)

    serializer = OrganizationServiceSerializer(data=data_to_create_service)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    initial_data = serializer.data

    return initial_data
    

def create_client_type(organization:Organization, name='testing client type', description='testing client type description', fields:list[tuple[str, FieldType]]=None) -> OrganizationClientType:

    if not fields:
        fields = [('testing field', FieldType.TEXT.value), ('testing field 2', FieldType.NUMBER.value)]

    return OrganizationClientType.objects.create(
        organization=organization,
        name=name,
        description=description,
        fields=fields,
        created_by=create_user(organization, username='test_user_client', email='client_test@email.com'))


def create_kumbio_token(app=AppToken):
    return KumbioToken.objects.create(app=app)


def create_professional(organization:Organization, user:KumbioUser=None, name='test professional'):
    if not user: 
        user =  create_user(organization, username='test_professional', email='anotheremail@gmail.com')
    
    return OrganizationProfessional.objects.create(
        organization=organization,
        kumbio_user=user,
        created_by=user)


class TestOrganizationCreation(APITestCase):
    
    def test_organization_creation(self):
        org = create_organization(use_user=True)
        self.assertEqual(org.name, 'test organization')

        # we got to check if the default client types were created for this organization
        
        self.assertEqual(org.client_types.count(), DEFAULT_CLIENT_TYPES.__len__())
    

class TestPlace(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.user = create_user(self.organization)
        self.set_authorization()
        
        self.data_to_create_place = {
            "place":{
                "organization" : self.organization.id,
                "address": "la calle de al lado",
                "name": "Dresden",
                "created_by": self.user.id
            },
            "days":[
                {
                    "week_day": 0,
                    "exclude": [[0, 7], [18, 23]],
                    "note": "Una nota de prueba"
                }
            ]
            
        }
        self.place = create_place(self.data_to_create_place, self.organization, self.user)
        
        Print('Testing setup for TestPlace completed')

    
    def test_place_creation(self):

        self.assertTrue(self.client.login(email=EMAIL, password=PASSWORD))

        initial_data = create_place(self.data_to_create_place, self.organization, self.user, create_with_serializer=True)
        
        del initial_data['created_at']
        del initial_data['id']

        url = reverse('organization_info:place')
        response = self.client.post(url, self.data_to_create_place, format='json').json()
        
        try:
            del response['created_at']
            del response['id']
        except KeyError:
            self.assertEqual('you are not authorized', '')
            

        # Print('New place created', response)

        self.assertEqual(response, initial_data)


    # helper functions ---------------------------------------------------------

    # Convert this set authorization in a global function
    def set_authorization(self):
        url = reverse('register:obtain_auth_token')
        # TODO: Check why we have to pass the email as username
        resp = self.client.post(url, {'username':EMAIL, 'password':PASSWORD, 'for_kumbio': True}, format='json')
    
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)


class TestOrganizationSector(APITestCase):

    def setUp(self) -> None:
        self.data_to_create_sector = dict(
            name='testing sector',
            description='testing sector description')
        self.user = create_user(create_organization())
        self.set_authorization()
        self.sector = create_organization_sector(self.data_to_create_sector)
        
    
    def test_create_sector(self):


        url = reverse('organization_info:sector')
        
        # Testing for one sector
        response = self.client.get(url, {'sector_id': 1}, format='json')

        sector_data_serialized = OrganizationSectorSerializer(self.sector)
        
        self.assertEqual(response.json(), [sector_data_serialized.data])

        # ---------------------------------------------------------
        # Testing for all sectors
        response = self.client.get(url, format='json')

        sectors = Sector.objects.all()
        sector_data_serialized = OrganizationSectorSerializer(sectors, many=True)

        self.assertEqual(response.json(), sector_data_serialized.data)



    def set_authorization(self):
        url = reverse('register:obtain_auth_token')
        # TODO: Check why we have to pass the email as username
        resp = self.client.post(url, {'username':EMAIL, 'password':PASSWORD, 'for_kumbio': True}, format='json')
        
        # Print('Response from auth', resp.json())
    
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)


class TestOrganizationClient(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.user = create_user(self.organization)
 

    def test_create_client_type(self):
        client_type = create_client_type(self.organization)
        self.assertTrue(client_type)
        self.assertEqual(client_type.name, 'testing client type')
        self.assertEqual(client_type.description, 'testing client type description')

    
    def test_create_client(self):
        
        client_type = create_client_type(self.organization)
        url = reverse('organization_info:client')

        # creating the data for the client

        dependent_from = {
            'first_name': 'parent first name',
            'last_name': 'parent last name',
            'email': 'parent@email.com',
            'phone': 'parent phone',
        }

        client_data = {
            'organization': self.organization.id,
            'type': client_type.pk, # type must come from the organization sector type
            'first_name': 'child',
            'last_name': 'child',
            'email': 'client@email.com',
            'phone': 'client phone',
        }

        data_to_create_client = {
            'client': client_data,
            'dependent_from': dependent_from,
        }
        
        # creating the request without using the credentials
        unauthorized_response = self.client.post(url, data_to_create_client, format='json')
        self.assertEqual(unauthorized_response.status_code, 401)

        # setting the authorization
        kumbio_token = create_kumbio_token(app=AppToken.CALENDAR).token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + kumbio_token)

        res = self.client.post(url, data_to_create_client, format='json')

        first_org_client:OrganizationClient = OrganizationClient.objects.get(pk=res.json()['id'])

        self.assertEqual(first_org_client.first_name, client_data['first_name'])
        self.assertEqual(first_org_client.dependent.first_name, dependent_from['first_name'])
        
        data_to_create_client['dependent_from']['same_as_client'] = True
        res = self.client.post(url, data_to_create_client, format='json')
        
        second_org_client:OrganizationClient = OrganizationClient.objects.get(pk=res.json()['id'])
        
        self.assertEqual(second_org_client.first_name, client_data['first_name'])
        self.assertEqual(second_org_client.dependent.first_name, client_data['first_name'])
        

class TestOrganizationProfesional(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.user = create_user(self.organization)
        self.sector = create_organization_sector()
        self.professional = create_professional(self.organization)
        
    
    def test_create_professional(self):
        url = reverse('organization_info:professional')

        # creating the data for the client

        pass