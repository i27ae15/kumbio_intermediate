# python 
import json
import os
# django
from django.urls import reverse
from .models.main_models import (Organization, OrganizationPlace, OrganizationService, Sector, OrganizationClient, 
                                 OrganizationClientType, OrganizationProfessional, DayAvailableForProfessional, DayAvailableForPlace)

from rest_framework.test import APITestCase

# models
from user_info.models import KumbioUser, KumbioUserRole
from .models.default_values import DEFAULT_CLIENT_TYPES

# serializers 
from .serializers.model_serializers import OrganizationPlaceSerializer, OrganizationServiceSerializer, OrganizationSectorSerializer, OrganizationClientSerializer, OrganizationClientDependentFromSerializer
from authentication_manager.models import KumbioToken, AppToken

# utils
from organization_info.utils.enums import FieldType

from print_pp.logging import Print


EMAIL='testuser@testuser.com'
PASSWORD = 'testuser'
USERNAME = 'testuser'

# TODO: move some if not all these function to a more general scope

def set_authorization(client):
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


def create_place(data_to_create_place:dict, organization:Organization, user:KumbioUser, create_with_serializer=False) -> 'OrganizationPlace | dict':
    # create a post
    place_object:OrganizationPlace = None
    place_data:dict = None
    
    if not create_with_serializer:
        place_object = OrganizationPlace.objects.create(
            organization=organization,
            created_by=user,
            address='testing address',
            name='testing name')

    else:
        serializer = OrganizationPlaceSerializer(data=data_to_create_place['place'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        place_object = serializer.instance
        place_data = serializer.data

    # create days available
    for day in range(0, 7):
        DayAvailableForPlace.objects.create(
            place=place_object,
            week_day=day,
            exclude=[[1, 8], [17, 23]])

    if create_with_serializer:
        return place_data

    return place_object


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


def create_kumbio_token(organization:Organization, app=AppToken):
    return KumbioToken.objects.create(app=app, organization=organization)


def create_professional(organization:Organization, place:OrganizationPlace, user:KumbioUser=None, name='test professional'):
    if not user: 
        user =  create_user(organization, username='test_professional', email='anotheremail@gmail.com')
    
    return OrganizationProfessional.objects.create(
        organization=organization,
        kumbio_user=user,
        place=place,
        created_by=user)


def create_client(organization:Organization, client_type:OrganizationClientType, num_clients=1) -> list[OrganizationClient]:
    clients = []

    for i in range(num_clients):
        dependent_from = {
            'first_name': 'parent first name' + str(i),
            'last_name': 'parent last name' + str(i),
            'email': 'parent@email.com' + str(i),
            'phone': 'parent phone' + str(i),
        }

        client_data = {
            'organization': organization.id,
            'type': client_type.pk, # type must come from the organization sector type
            'first_name': 'child' + str(i),
            'last_name': 'child' + str(i),
            'email': 'client@email.com' + str(i),
            'phone': 'client phone' + str(i),
        }


        extra_fields:list[tuple] = client_type.fields

        converted_extra_fields:list[list] = []

        for index, field in enumerate(extra_fields):
            field = list(field)

            if field[1] == 'TEXT':
                field.append('value' + str(index))
            
            elif field[1] == 'NUMBER':
                num = int(f'{index}0{i}')
                field.append(num)

            converted_extra_fields.append(field)

        client_data['extra_fields'] = converted_extra_fields

        data_to_create_client = {
            'client': client_data,
            'dependent_from': dependent_from,
        }

        clients.append(data_to_create_client)


    data_from_serializer:list[OrganizationClient] = list()

    for client in clients:
        client_serializer = OrganizationClientSerializer(data=client['client'])
        client_serializer.is_valid(raise_exception=True)
        client_serializer.save()

        client['dependent_from']['client'] = client_serializer.data['id']
        dependent_from_serializer = OrganizationClientDependentFromSerializer(data=client['dependent_from'])
        dependent_from_serializer.is_valid(raise_exception=True)
        dependent_from_serializer.save()

        client_instance:OrganizationClient = client_serializer.instance
        client_serializer = OrganizationClientSerializer(client_instance)

        data_from_serializer.append(client_serializer.instance)

    return data_from_serializer
  

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
                },
                {
                    "week_day": 1,
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
        response = self.client.post(url, self.data_to_create_place, format='json')
        res = response.json()

        try:
            del res['created_at']
            del res['id']
        except KeyError:
            Print('error with response', res)
            self.assertEqual('you are not authorized', '')
            
        

        self.assertEqual(response.status_code, 201)


    def test_get_place(self):
        self.assertTrue(self.client.login(email=EMAIL, password=PASSWORD))
        create_place(self.data_to_create_place, self.organization, self.user, create_with_serializer=True)

        url = reverse('organization_info:place')
        response = self.client.get(url, format='json').json()


    def test_update_place(self):
        self.assertTrue(self.client.login(email=EMAIL, password=PASSWORD))
        for i in range(0, 10):
            self.data_to_create_place['place']['address'] = 'la calle de al lado' + str(i)
            create_place(self.data_to_create_place, self.organization, self.user, create_with_serializer=True)
        
        self.data_to_create_place['place']['address'] = 'la calle de al lado 115'
        place = create_place(self.data_to_create_place, self.organization, self.user, create_with_serializer=True)

        url = reverse('organization_info:place')
        response = self.client.get(url, format='json').json()
        place_id = response[-1]['id']


        self.assertEqual(place['id'], place_id)
   
        data_to_update = {
            'place_id': 8,
            'place_data': {'address': 'la nueva calle de al lado'}
        }

        response = self.client.put(url, data_to_update, format='json').json()
        response = self.client.get(url, format='json').json()

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
        main_url = reverse('organization_info:client')
        url_for_client_type = reverse('organization_info:client_types')

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
        unauthorized_response = self.client.post(main_url, data_to_create_client, format='json')
        self.assertEqual(unauthorized_response.status_code, 401)

        # setting the authorization
        kumbio_token = create_kumbio_token(organization=self.organization, app=AppToken.CALENDAR).token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + kumbio_token)

        client_types:list = self.client.get(url_for_client_type, format='json').json()
         
        extra_fields:list[list] = client_types[0]['fields']

        for index, field in enumerate(extra_fields):
            if field[1] == 'TEXT':
                field.append('value' + str(index))
            
            elif field[1] == 'NUMBER':
                field.append(index)

        client_data['extra_fields'] = extra_fields

        res = self.client.post(main_url, data_to_create_client, format='json')

        try:
            first_org_client:OrganizationClient = OrganizationClient.objects.get(pk=res.json()['id'])
        except KeyError as e:
            self.fail(res.json())

        self.assertEqual(first_org_client.first_name, client_data['first_name'])
        self.assertEqual(first_org_client.dependent.first_name, dependent_from['first_name'])
        
        data_to_create_client['dependent_from']['same_as_client'] = True
        res = self.client.post(main_url, data_to_create_client, format='json')
        
        second_org_client:OrganizationClient = OrganizationClient.objects.get(pk=res.json()['id'])
        
        self.assertEqual(second_org_client.first_name, client_data['first_name'])
        self.assertEqual(second_org_client.dependent.first_name, client_data['first_name'])
    

    def test_get_clients(self):
        client_type = create_client_type(self.organization)
        main_url = reverse('organization_info:client')
        # url_for_extra_fields = reverse('organization_info:extra_fields_for_client_type')
        url_for_client_type = reverse('organization_info:client_types')
        
        kumbio_token = create_kumbio_token(organization=self.organization, app=AppToken.CALENDAR)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + kumbio_token.token)

        client_types:list = self.client.get(url_for_client_type, format='json').json()
        client_type:OrganizationClientType = OrganizationClientType.objects.get(pk=client_types[0]['id'])
        # creating the data for the client

        num_clients = 10
        clients = create_client(self.organization, client_type, num_clients=num_clients)
        self.assertEqual(len(clients), num_clients)

        res = self.client.get(main_url, {'client_id': clients[0].pk}, format='json')

        self.assertEqual(len(res.json()), 1)

    
    def test_delete_clients(self):
        create_client(self.organization, create_client_type(self.organization))
        main_url = reverse('organization_info:client')

        kumbio_token = create_kumbio_token(organization=self.organization, app=AppToken.CALENDAR)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + kumbio_token.token)
        
        res = self.client.delete(main_url, format='json')
        Print(res.json())
        self.assertEqual(res.status_code, 200)

        res = self.client.delete(main_url, {'client_id': 10}, format='json')
        self.assertEqual(res.status_code, 404)

        res = self.client.delete(main_url, {'client_id': 1}, format='json')
        self.assertEqual(res.status_code, 204)



class TestOrganizationProfesional(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.user = create_user(self.organization)
        self.sector = create_organization_sector()
        self.place = create_place({}, self.organization, self.user)
        self.professional = create_professional(self.organization, place=self.place)
        self.service = create_service({}, self.organization)
        
    
    def test_create_professional(self):

        professional_days = DayAvailableForProfessional.objects.filter(professional=self.professional)
        place_days = DayAvailableForPlace.objects.filter(place=self.place)

        data_to_create_professional = {
            'email': 'andresruse18@gmail.com',
            'first_name': 'Andres',
            'last_name': 'Ruse',
            'phone': '123456789',
            'username':'andresruse',
            'organization': self.organization.pk,
            'password': '123456789'
        }

        self.assertEqual(len(professional_days), len(place_days))


    def test_update_professional(self):

        set_authorization(self.client)

        url = reverse('organization_info:professional')

        # Abre el archivo JSON
        root = os.path.join("organization_info", "test.json")
        with open(root, "r") as f:
            # Lee el contenido del archivo como una cadena de texto
            data_json = f.read()

        # Convierte la cadena de texto en un objeto de Python (diccionario)
        data = json.loads(data_json)

        # Ahora puedes trabajar con el objeto de Python como lo desees
        data_to_update_professional = {
            'professional_id': self.professional.pk,
            'professional_data': {
                'services_ids': [self.service.pk],
                'created_by_id': self.user.pk,
                'kumbio_user_id': self.professional.kumbio_user.pk,
                'organization_id': self.organization.pk,
                'place_id': self.place.pk,
                'place': {}
            },
            'days': [{
                'week_day': 0,
                'exclude': [[0, 10], [18, 23]],
                'note': 'Before update'
            }]
        }

        res = self.client.put(url, data, format='json')
        

        data['days'][0] = {
            'week_day': 0,
            'exclude': [[0, 12], [18, 23]],
            'note': 'After update'
        }

        data['professional_data']['services_ids'] = []
        res = self.client.put(url, data, format='json')
        
class TestOrganizationService(APITestCase):
    
        def setUp(self) -> None:
            self.organization = create_organization()
            self.user = create_user(self.organization)
            self.sector = create_organization_sector()
            self.place = create_place({}, self.organization, self.user)
            self.professional = create_professional(self.organization, place=self.place)
            self.service = create_service({}, self.organization)
            set_authorization(self.client)
            
        
        def test_create_service(self):
            url = reverse('organization_info:service')
            self.professional.services.add(self.service)

            res = self.client.get(url, format='json')
            self.assertEqual(res.status_code, 200)


