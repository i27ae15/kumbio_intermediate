from django.core.management.base import BaseCommand
from django.utils import timezone
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html

import os

from faker import Faker
from dotenv import load_dotenv
from print_pp import Print

# models
from organization_info.models.main_models import Organization

from user_info.models import KumbioUser, KumbioUserRole, KumbioUserPermission


# serializers
from user_info.serializers import CreateKumbioUserSerializer

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

class Command(BaseCommand):
    help = 'This will fill the database with test data'


    def handle(self, *args, **kwargs):

        if not os.getenv('USE_LOCAL_DB'):
            self.stdout.write('USE_LOCAL_DB is not set to True')
            return
        
        self.create_user_roles()
        self.create_users()
        # first we need to create te organization to associate the user with it
    
    def create_user_roles(self):        
        for role in USER_ROLES:
            KumbioUserRole.objects.create(**role)

    
    def create_users(self) -> KumbioUser:

        for i in range(11):
            
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

        return user
    

    def create_organization(self, user_data:dict) -> Organization:

        organization:Organization = Organization.objects.create(
            # org info
            name=fake.company(),
            email=user_data['email'],
            phone=user_data['phone'],
            
            # owner info
            owner_email=user_data['email'],
            owner_first_name=user_data['first_name'],
            owner_last_name=user_data['last_name'],
            owner_phone=user_data['phone'],
        )
        return organization
