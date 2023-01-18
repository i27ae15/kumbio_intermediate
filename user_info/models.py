# python
import requests
import datetime
import sys
import os

# django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# models 

# utils
from utils.numbers import random_with_N_digits



# notifications
from kumbio_communications import send_notification

from print_pp.logging import Print

from dotenv import load_dotenv

load_dotenv()

# TODO: User environ instead of hardcode
TOKEN_FOR_CALENDAR = os.environ['TOKEN_FOR_CALENDAR']
CALENDAR_ENDPOINT = os.environ['CALENDAR_ENDPOINT']


class KumbioUserPermission(models.Model):
    name:str = models.CharField(max_length=100)
    description:str = models.TextField()
    
    def __str__(self):
        return self.name


class KumbioUserRole(models.Model):
    name:str = models.CharField(max_length=50)
    description:str = models.CharField(max_length=200)
    permissions = models.ManyToManyField(KumbioUserPermission, blank=True)
    
    def __str__(self):
        return self.name


# --------------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------------

class NotificationsSettings(models.Model):

    user:'KumbioUser' = models.ForeignKey('KumbioUser', on_delete=models.CASCADE)

    # notifications preferences
    appointment_confirmation:bool = models.BooleanField(default=True)
    appointment_reschedule:bool = models.BooleanField(default=True)
    appointment_cancellation:bool = models.BooleanField(default=True)

    day_briefing:bool = models.BooleanField(default=True)
    time_to_receive_briefing:datetime.time = models.TimeField(default=datetime.time(8, 0, 0))

    # deliver method

    email:bool = models.BooleanField(default=True)
    sms:bool = models.BooleanField(default=False)
    whatsapp:bool = models.BooleanField(default=False)

    # this should only be use for admin users
    low_inventory:bool = models.BooleanField(default=False)


class KumbioUserManager(BaseUserManager):
    def create_user(self, email, username, organization, password=None, **extra_fields):
        
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username,
            organization=organization,
            **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class KumbioUser(AbstractBaseUser, PermissionsMixin):
    
    # foreignkeys 
    
    organization = models.ForeignKey('organization_info.Organization', null=True, default=None, on_delete=models.CASCADE, related_name='organization_user')
    role:KumbioUserRole = models.ForeignKey(KumbioUserRole, on_delete=models.CASCADE, null=True, default=None)
    
    extra_permissions = models.ManyToManyField(KumbioUserPermission, blank=True)
    
    # -----------------------------------------------------------
    # fields 

    # this must be one just for the moment
    available_places = models.ManyToManyField('organization_info.OrganizationPlace', blank=True, related_name='available_places')
    available_services = models.ManyToManyField('organization_info.OrganizationService', blank=True, related_name='available_services')
    
    code_to_verify_email:str = models.CharField(max_length=256, default=None, null=True)
    
    email:str = models.EmailField(max_length=255, unique=True)
       
    first_name:str = models.CharField(max_length=255)
        
    is_active:bool = models.BooleanField(default=True)
    is_staff:bool = models.BooleanField(default=False)
    is_tester:bool = models.BooleanField(default=False)
    is_email_verified:bool = models.BooleanField(default=False)
        
    last_name:str = models.CharField(max_length=255)
    
    objects = KumbioUserManager()
    
    phone:str = models.CharField(max_length=120, default='')

    registration_date:datetime.datetime = models.DateTimeField(default=timezone.now)
    
    username:str = models.CharField(max_length=255, unique=True)
    
    # tokens
    
    calendar_token:str = models.CharField(max_length=255, default=None, null=True)
    selene_token:str = models.CharField(max_length=255, default=None, null=True)
    
    # USER PERMISSIONS 
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    # properties
    # -------------------------------------------------------------------

    @property
    def notifications_settings(self) -> NotificationsSettings:
        return self.notificationssettings_set.all()[0] 

    # functions
    # -------------------------------------------------------------------

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


    def get_short_name(self):
        return self.username
    
    
    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True
    
    
    def send_verification_code(self, save=True):
        self.code_to_verify_email = random_with_N_digits(6)
        if save:
            self.save()
        
        send_notification(token_for_app=TOKEN_FOR_CALENDAR, 
                          organization_id=self.organization.id if self.organization else 0,
                          send_to=[self.email],
                          messages=[f'Your verification code is {self.code_to_verify_email}'],
                          subjects=['Verify your email'])
        
    
    def verify_code(self):
        self.is_email_verified = True
        self.code_to_verify_email = None
        self.save()
        
    
    def set_role(self, role:KumbioUserRole):
        self.role = role
        self.save()
    

    def save(self, *args, **kwargs):
        first_time = True if not self.pk else False
        if not self.pk and not kwargs.get('set_verified_email') and not 'test' in sys.argv:
            self.send_verification_code(save=False)
            # by default create the settings for the notifications
        
        elif kwargs.get('set_verified_email'):
            self.is_email_verified = True

        try:
            del kwargs['set_verified_email']
        except KeyError:
            pass
            # we set pass here because we need to assure that set_verified_email is not in kwargs, so, if key_error is raised, we just pass
        
        super().save(*args, **kwargs)
        
        if first_time:
            # creating the user in the calendar app so we can obtain the token for the user in calendar
            if not 'test' in sys.argv:
                res = requests.post(f'{CALENDAR_ENDPOINT}register/api/v2/create-user/', json={
                    'organization_id': self.organization.id,
                    'email': self.email,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'kumbio_user_id': self.pk,
                    # TODO: change this to the role of the user
                    'role': self.role.pk if self.role else 1,
                })
                
                self.calendar_token = res.json()['token']
            else:
                self.calendar_token = 'token-test-for-calendar'

            NotificationsSettings.objects.create(user=self)


    def __str__(self):
        try: return f'{self.id} - {self.email} - {self.organization.name}'
        except Exception: return f'{self.pk} - {self.email} - {self.organization}'


