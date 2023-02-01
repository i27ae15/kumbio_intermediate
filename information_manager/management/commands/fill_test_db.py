import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import QuerySet
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html

import os

from faker import Faker
from dotenv import load_dotenv
from print_pp import Print

# models
from organization_info.models.main_models import (Organization, OrganizationClient, OrganizationClientType, OrganizationProfessional, OrganizationService, 
PaymentMethodAcceptedByOrg, ProfessionalSpecialty, Sector, OrganizationPlace, ClientParent)

from user_info.models import KumbioUser, KumbioUserRole, KumbioUserPermission


from organization_info.utils.enums import FieldType

# serializers
from organization_info.serializers.model_serializers import (DayAvailableForProfessionalSerializer, ClientParentSerializer,
OrganizationClientSerializer, OrganizationProfessionalSerializer, OrganizationServiceSerializer, OrganizationPlaceSerializer,
DayAvailableForPlaceSerializer)
from user_info.serializers.serializers import CreateKumbioUserSerializer

# kumbio_user_serializer = CreateKumbioUserSerializer(data=body_data, context={'set_verified_email': True})
# kumbio_user_serializer.is_valid(raise_exception=True)


load_dotenv()
fake = Faker()
Faker.seed(115)


USER_ROLES = [
    {
        'name': 'organization_owner',
        'description': 'Organization owner'
    },
    {
        'name': 'organization_admin',
        'description': 'Organization admin'
    },
    {
        'name': 'organization_professional',
        'description': 'Organization professional'
    }
]


PAYMENT_METHODS = [
    'CASH',
    'DEBIT_CARD',
    'CREDIT_CARD',
    'PAYPAL',
    'VENMO',
    'ZELLE',
    'APPLE_PAY',
    'GOOGLE_PAY',
    'CASH_APP',
]


DEFAULT_SECTORS = [
    'AUTOMOTIVE',
    'BEAUTY',
    'BUSINESS',
    'EDUCATION',
    'MEDICAL',
]


class Command(BaseCommand):
    help = 'This will fill the database with test data'


    def handle(self, *args, **kwargs):

        if not os.getenv('USE_LOCAL_DB'):
            self.stdout.write('USE_LOCAL_DB is not set to True')
            return
        
        # static values creation
        self.stdout.write('-' * 50)
        self.stdout.write('creating default values: user_roles, payment_methods, organization_sectors')
        
        self.create_user_roles()
        self.create_payment_methods()
        self.create_sectors()
        
        self.stdout.write('created default values')
        self.stdout.write('-' * 50)

        self.create_users()
        self.create_organization_services()
        self.create_places()
        self.create_specialties()
        self.create_professionals()
        self.create_clients()
    

    def create_user_roles(self):        
        for role in USER_ROLES:
            KumbioUserRole.objects.create(**role)


    def create_payment_methods(self):    
        for method in PAYMENT_METHODS:
            PaymentMethodAcceptedByOrg.objects.create(payment_method=method)


    def create_sectors(self):
        for sector in DEFAULT_SECTORS:
            Sector.objects.create(name=sector, description=sector)

    
    def create_users(self) -> KumbioUser:
        USERS_TO_CREATE = 3
        self.stdout.write('-' * 50)
        self.stdout.write(f'Creating {USERS_TO_CREATE} organization owners users')

        for i in range(USERS_TO_CREATE):
            
            if i == 0:
                # create superuser
                user_data = {
                    'first_name': 'Andres',
                    'last_name': 'Melendes',
                    'email': 'andresruse18@gmail.com',
                    'phone': '0414-1234567',
                    'password': 'ruse18775',
                    'username': 'i27ae15',
                    'role': 1,
                }
            else:
                user_data = {
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.email(),
                    'phone': fake.phone_number(),
                    'password': fake.password(),
                    'username': fake.user_name() + '_test',
                    'role': 1,
                }

            organization:Organization = self.create_organization(user_data)

            user_data['organization'] = organization.pk
            # then we create the user

            kumbio_user_serializer = CreateKumbioUserSerializer(data=user_data, context={'set_verified_email': True})
            kumbio_user_serializer.is_valid(raise_exception=True)
            kumbio_user_serializer.save()

            user:KumbioUser = kumbio_user_serializer.instance
            user.set_password(user_data['password'])
            
            if i == 0:
                user.is_active = True
                user.is_staff = True
                user.is_admin = True
                user.save()

        self.stdout.write(f'Users created successfully; total {USERS_TO_CREATE}')
        self.stdout.write('-' * 50)
        return user
    

    def create_organization(self, user_data:dict) -> Organization:

        payment_methods = [n + 1 for n in range(len(PAYMENT_METHODS))]
        sector = random.choice(Sector.objects.all())

        organization:Organization = Organization.objects.create(
            # org info
            name=fake.company(),
            sector=sector,
            email=user_data['email'],
            phone=user_data['phone'],            
            # owner info
            owner_email=user_data['email'],
            owner_first_name=user_data['first_name'],
            owner_last_name=user_data['last_name'],
            owner_phone=user_data['phone'],
        )
        organization.payment_methods_accepted.set(payment_methods)
        return organization


    def create_organization_services(self):

        SERVICES_TO_CREATE = 1
        self.stdout.write('-' * 50)
        self.stdout.write(f'Creating {SERVICES_TO_CREATE} services per organization')

        organizations = Organization.objects.all()

        for org in organizations:
            for _ in range(SERVICES_TO_CREATE):
                service_data = {
                    'organization': org.pk,
                    'service': fake.job(),
                    'description': fake.text(),
                    'time_interval': random.choice([.25, .5, .75, 1]),
                    'price': fake.pyint(),
                    'buffer': random.choice([0, .25, .5, .75, 1]),
                }
                serializer = OrganizationServiceSerializer(data=service_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        
        self.stdout.write(f'Services created successfully; total: {SERVICES_TO_CREATE * organizations.count()}')
        self.stdout.write('-' * 50)
    

    def create_places(self):

        RANGE_LIMIT = 1
        self.stdout.write('-' * 50)
        self.stdout.write(f'Creating {RANGE_LIMIT} places per organization')

        organizations = Organization.objects.all()
        payment_methods = [n + 1 for n in range(len(PAYMENT_METHODS))]

        for org in organizations:
            services:QuerySet[OrganizationService] = OrganizationService.objects.filter(organization=org)
            for _ in range(RANGE_LIMIT):
                place_data = {
                    'organization': org.pk,
                    'address': fake.address(),
                    'admin_email': org.email,
                    'additional_info': fake.text(),
                    'description': fake.text(),
                    'important_information': fake.text(),
                    'phone': org.phone,
                    'local_time_zone': 'America/Caracas',
                    'name': fake.street_name(),
                    'created_by': 1,
                }
                serializer = OrganizationPlaceSerializer(data=place_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # Once save, we need to create the days available for that place
                place:OrganizationPlace = serializer.instance
                
                place.services.set([service.pk for service in services])
                place.payment_methods_accepted.set(payment_methods)
                
                self.create_place_days(place)

        self.stdout.write(f'Places created successfully; total: {RANGE_LIMIT * organizations.count()}')
        self.stdout.write('-' * 50)


    def create_place_days(self, place:OrganizationPlace):
        for day in range(5):
            day_data = {
                'place': place.pk,
                'week_day': day,
                'exclude': [[0, random.randint(5, 8)], [random.randint(10, 12), random.randint(13, 16)], [random.randint(17, 20), 23]],
                'note': fake.text(),
            }
            serializer = DayAvailableForPlaceSerializer(data=day_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()


    def create_specialties(self):
        organizations = Organization.objects.all()

        RANGE_LIMIT = 1
        total_specialties = 0
        self.stdout.write('-' * 50)
        self.stdout.write(f'Creating professional specialties between 1 & {RANGE_LIMIT}')

        for org in organizations:
            for _ in range(RANGE_LIMIT):
                ProfessionalSpecialty.objects.create(
                    organization=org,
                    name=fake.job(),
                    created_by=KumbioUser.objects.get(id=1),
                )
            total_specialties += 1

        self.stdout.write(f'Specialties created successfully; total: {total_specialties}')
        self.stdout.write('-' * 50)


    def create_professionals(self):

        RANGE_LIMIT = 1
        total_professionals = 0
        self.stdout.write('-' * 50)
        self.stdout.write(f'Creating professionals: {RANGE_LIMIT} per organization')
        
        organizations = Organization.objects.all()

        for org in organizations:
            services:QuerySet[OrganizationService] = OrganizationService.objects.filter(organization=org)
            specialties:QuerySet[ProfessionalSpecialty] = ProfessionalSpecialty.objects.filter(organization=org)
            places:QuerySet[OrganizationPlace] = OrganizationPlace.objects.filter(organization=org)

            for _ in range(RANGE_LIMIT):
                professional_data = {
                    'organization_id': org.pk,

                    'place_id': random.choice(places).pk,

                    'academic_information': fake.text(),
                    'about_me': fake.text(),
                    'identification_number': fake.pyint(),
                    'certification_number': fake.pyint(),
                    'custom_price': [{'place_id': 0, 'price': fake.pyint()}],
                    'created_by_id': 1,
                }
                
                user = self.create_kumbio_user(org)
                professional_data['kumbio_user_id'] = user.pk
            
                serializer = OrganizationProfessionalSerializer(data=professional_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                professional:OrganizationProfessional = serializer.instance

                professional.services.set([service.pk for service in services])
                professional.specialties.set([specialty.pk for specialty in specialties])
                professional.kumbio_user.available_places.set([place.pk for place in places])
                professional.kumbio_user.available_services.set([service.pk for service in services])

                self.create_professional_days(professional)
                total_professionals += 1
        

        self.stdout.write(f'Professionals created successfully; total: {total_professionals}')
        self.stdout.write('-' * 50)
    

    def create_professional_days(self, professional:OrganizationProfessional):

        services:QuerySet[OrganizationService] = OrganizationService.objects.filter(organization=professional.organization.pk)

        for day in range(1):
            day_data = {
                'professional': professional.pk,
                'week_day': day,
                'exclude': [[0, random.randint(5, 8)], [random.randint(10, 12), random.randint(13, 16)], [random.randint(17, 20), 23]],
                'services':{service.pk: {'time_interval': service.time_interval} for service in services},
                'note': fake.text(),
            }
            serializer = DayAvailableForProfessionalSerializer(data=day_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            

    def create_kumbio_user(self, org:Organization) -> KumbioUser:
        user_data = {
            'organization': org.pk,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'password': fake.password(),
            'username': fake.password(length=5, special_chars=False, digits=True, upper_case=False, lower_case=True),
            'role': 2,
        }

        kumbio_user_serializer = CreateKumbioUserSerializer(data=user_data, context={'set_verified_email': True})
        kumbio_user_serializer.is_valid(raise_exception=True)
        kumbio_user_serializer.save()

        return kumbio_user_serializer.instance

    
    def create_clients(self):
        RANGE_LIMIT = 2
        total_clients = 0
        self.stdout.write('-' * 50)
        self.stdout.write(f'Creating clients: {RANGE_LIMIT} * org.num_professionals()')
        
        organizations = Organization.objects.all()

        for org in organizations:
            client_types:QuerySet[OrganizationClientType] = OrganizationClientType.objects.filter(organization=org)
            professionals:int = OrganizationProfessional.objects.filter(organization=org).count()

            range_to_create = RANGE_LIMIT * professionals

            for _ in range(range_to_create):
                client_type = random.choice(client_types)

                extra_fields:list[list] = list()

                for field in  client_type.fields:
                    
                    if field[1] == FieldType.NUMBER.value:
                        extra_fields.append([field[0], field[1], fake.pyint()])
                    elif field[1] == FieldType.TEXT.value:
                        extra_fields.append([field[0], field[1], fake.text()])


                client_data = {
                    'organization': org.pk,
                    'type': client_type.pk,
                    'extra_fields': extra_fields,
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'referral_link': fake.url(),
                    'created_by_user': 1,
                    'created_by_app': 3
                }

                same_as_client = random.choice([True, False])

                if same_as_client:
                    client_dependent_data = {
                        'first_name': client_data['first_name'],
                        'last_name': client_data['last_name'],
                        'email': fake.email(),
                        'phone': fake.phone_number(),
                        'same_as_client': True,
                    }
                else:
                    client_dependent_data = {
                        'first_name': fake.first_name(),
                        'last_name': fake.last_name(),
                        'email': fake.email(),
                        'phone': fake.phone_number(),
                        'same_as_client': False,
                    }


                serializer = ClientParentSerializer(data=client_dependent_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                client_parent:ClientParent = serializer.instance

                client_data['client_dependent'] = client_parent.pk
                serializer = OrganizationClientSerializer(data=client_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                total_clients += 1
        
        self.stdout.write(f'Clientes created successfully; total: {total_clients}')
        self.stdout.write('-' * 50)
        