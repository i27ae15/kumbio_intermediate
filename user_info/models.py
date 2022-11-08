# python
import os
import datetime

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
from utils.send_email import SendEmail
from utils.numbers import random_with_N_digits


# notifications
from kumbio_notifications.notifications import send_notification

from print_pp.logging import Print

from dotenv import load_dotenv

load_dotenv()

TOKEN_FOR_CALENDAR = "Token Calendar-90b150bc4c827d4ca6828006ce7097be17b8b41150"


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
                          organization_id=self.organization.pk,
                          send_to=['andresruse18@gmail.com'],
                          messages=[f'Your verification code is {self.code_to_verify_email}'],
                          subjects=['Verify your email'])
        
    
    def verify_code(self):
        self.is_email_verified = True
        self.code_to_verify_email = None
        self.save()

    
    def save(self, *args, **kwargs):
        if not self.pk and not kwargs.get('set_verified_email'):
            self.send_verification_code(save=False)
        
        elif kwargs.get('set_verified_email'):
            print('-'*100)
            print('verified email')
            print('-'*100)
            self.is_email_verified = True
            del kwargs['set_verified_email']
            
        super().save(*args, **kwargs)


    def __str__(self):
        try: return f'{self.id} - {self.email} - {self.organization.name}'
        except Exception: return f'{self.id} - {self.email} - {self.organization}'


