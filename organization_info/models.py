# python
import secrets
import datetime
import os
from dotenv import load_dotenv

# django
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models.query import QuerySet

# utils
from utils.send_email import SendEmail
from utils.numbers import random_with_N_digits

load_dotenv()


class Plan(models.Model):
    description:str = models.TextField()
        
    max_number_of_users:int = models.IntegerField(default=1)
    max_number_of_calendars:int = models.IntegerField(default=2)
    max_number_of_appoinments:int = models.IntegerField(default=150)

    name:str = models.CharField(max_length=100)
    
    price:float = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


# Integer choices ---------------------------------------------------------------
class Sector(models.Model):
    name:str = models.CharField(max_length=100)
    description:str = models.TextField()

# DB Models ---------------------------------------------------------------------


class Organization(models.Model):
    
    # Foreign Keys -----------------------------------------------------------
    plan:Plan = models.ForeignKey(Plan, on_delete=models.CASCADE, default=1)
    sector:Sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=True)
    id:str = models.CharField(max_length=100, primary_key=True)
    
    # ------------------------------------------------------------------------
    # Fields -----------------------------------------------------------------

    # data
    
    cancelation_policy:str = models.TextField(null=True, blank=True)
    country:str = models.CharField(max_length=120, default='')
    
    data_policy:str = models.TextField(null=True, blank=True)
    description:str = models.CharField(max_length=120, default='')
    
    email:str = models.EmailField(unique=True)
    
    invitation_link:str = models.CharField(max_length=256, unique=True, null=True, default=None)
    
    link_dashboard:str = models.CharField(max_length=120, null=True, blank=True)
    logo = models.ImageField(upload_to='organization_logos', null=True, blank=True)
    
    name:str = models.CharField(max_length=120, unique=True)
    notification_email:str = models.EmailField(default=os.environ['DEFAULT_EMAIL'])
    notification_email_password = models.BinaryField(default=os.environ['DEFAULT_EMAIL_PASSWORD'].encode())

    phone:str = models.CharField(max_length=120)
    
    rating:float = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    website:str = models.CharField(max_length=120, null=True, blank=True)
    
    # owner data

    owner_email:str = models.EmailField()
    owner_first_name:str = models.CharField(max_length=120)
    owner_last_name:str = models.CharField(max_length=120)
    owner_phone:str = models.CharField(max_length=120)


    # ------------------------------------------------------------------------
    # Logs -------------------------------------------------------------------
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)


    # Properties -------------------------------------------------------------
    @property
    def services(self) -> QuerySet:
        return self.calendarcategory_set.all()       
    
    @property
    def professionals(self) -> QuerySet['KumbioUser']:
        return self.kumbiouser_set.all()
    
    
    # TODO: this must come from calendar api
    @property
    def calendars(self) -> QuerySet:
        # perform a query to get all calendars to the calendar api
        
        return self.calendar_set.all()
    

    @property
    def number_of_professionals(self) -> int:
        return self.professionals.count()


    @property
    def number_of_services(self) -> int:
        return self.services.count()
    

    # call a request to the calendar api to get the number of calendars
    @property
    def number_of_calendars(self) -> int:
        return self.calendars.count()
    

    # call a request to the calendar api to get the number of appoinments
    @property
    def number_of_appointments(self) -> int:
        return self.appointment_set.count()
        
        
    # other methods    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.invitation_link = secrets.token_urlsafe(21)
            self.id = secrets.token_urlsafe(21)
        super().save(*args, **kwargs)
                
        
    def __str__(self) -> str:
        return f'{self.id} - {self.name} - {self.email}'


class PaymentMethodAcceptedByOrg(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    payment_method:str = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.id} - {self.organization.name} - {self.payment_method}'


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
    
    organization:Organization = models.ForeignKey(Organization, null=True, default=None, on_delete=models.CASCADE)
    
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
    role:int = models.IntegerField(default=2)

    default_template_starts_at:int = models.IntegerField(default=0)
    
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
            
        SendEmail(
            self.organization.id, 
            self.email,
            'Verify your email',
            f'Your verification code is {self.code_to_verify_email}',
        )
        
    
    def verify_code(self):
        self.is_email_verified = True
        self.code_to_verify_email = None
        self.save()

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.send_verification_code(save=False)
            
        super().save(*args, **kwargs)


    def __str__(self):
        try: return f'{self.id} - {self.email} - {self.organization.name}'
        except Exception: return f'{self.id} - {self.email} - {self.organization}'


class Service(models.Model):
    
    # ---------------------------------------------------------------
    # Foreign Keys
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, default=None)
    # ---------------------------------------------------------------
    # Fields
    
    service:str = models.CharField(max_length=100)

    description:str = models.TextField(blank=True, null=True)

    time_interval:float = models.FloatField(default=1)

    # logs fields
    created_at:datetime.datetime = models.DateTimeField(default=datetime.datetime.utcnow)

    deleted_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='service_deleted_by')

    updated_at:datetime.datetime = models.DateTimeField(null=True, default=None)
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='service_updated_by')

        
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
    

    @property
    def is_updated(self) -> bool:
        return self.updated_at is not None


    def set_updated_by(self, user:KumbioUser):
        self.updated_by = user
        self.save()


    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.datetime.utcnow()
        else:
            self.updated_at = datetime.datetime.utcnow()
            
        # if not self.calendar.can_create_categories():
        #     raise ValidationError('This calendar has reached the maximum number of categories allowed.')
                    
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.deleted_at = datetime.datetime.utcnow()
        self.deleted_by = kwargs.get('user')
        self.save()
    
    
    def __str__(self) -> str:
        return f'{self.id} {self.organization.name} - {self.category}'


class Office(models.Model):
    # foreignkeys
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    # fields

    address:str = models.CharField(max_length=255)
    accepts_children:bool = models.BooleanField(default=True)
    accepts_pets:bool = models.BooleanField(default=True)
    additional_info:str = models.CharField(max_length=255)

    email:str = models.EmailField(max_length=255, unique=True)

    name:str = models.CharField(max_length=255)

    phone:str = models.CharField(max_length=255)

    schedule:str = models.CharField(max_length=255)

    photo:str = models.CharField(max_length=255)
    payment_methods = models.ManyToManyField(PaymentMethodAcceptedByOrg, blank=True)

    services:QuerySet = models.ManyToManyField(Service)


    # -----------------------------------------------------------
    # Logs 
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:KumbioUser = models.ForeignKey(KumbioUser, on_delete=models.CASCADE, related_name='office_created_by')
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='office_updated_by')
    deleted_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='office_deleted_by')

    # -----------------------------------------------------------
    # Properties

    # -----------------------------------------------------------
    # Methods

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.payment_methods:
                self.payment_methods.add(*PaymentMethodAcceptedByOrg.objects.filter(organization=self.organization))
            
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f'{self.name} - {self.organization.name}'


class Speciality(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    name:str = models.CharField(max_length=255)

    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:KumbioUser = models.ForeignKey(KumbioUser, on_delete=models.CASCADE, related_name='professional_created_by')
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='professional_updated_by')
    
    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'


class Professional(models.Model):

    # foreignkeys
    
    organization:Organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    
    # -----------------------------------------------------------
    # fields
    academic_formation:str = models.TextField(default='')
    about_me:str = models.TextField(default='')
    
    certificates = models.FileField(upload_to=f'{organization.name}-{organization.id}/professionals/certificates/', null=True, blank=True)
    
    email:str = models.EmailField(max_length=255, unique=True)
    experience:str = models.TextField(default='')
    
    first_name:str = models.CharField(max_length=255)
    
    last_name:str = models.CharField(max_length=255)
    
    phone:str = models.CharField(max_length=120, default='')
    photos = models.FileField(upload_to=f'{organization.name}-{organization.id}/professionals/photos/', null=True, blank=True)
    profile_picture:str = models.CharField(max_length=120, default='')
    
    specialities:QuerySet[Speciality] = models.ManyToManyField(Speciality)

    # -----------------------------------------------------------
    # Logs 
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:KumbioUser = models.ForeignKey(KumbioUser, on_delete=models.CASCADE, related_name='professional_created_by')
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='professional_updated_by')
    deleted_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='professional_deleted_by')
    
    # -----------------------------------------------------------
    # properties
    
    @property
    def services(self) -> QuerySet:
        return self.professionalservice_set.all()
    
    @property
    def number_of_services(self) -> int:
        return self.services.count()


    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    # -----------------------------------------------------------
    # methods
        
    def __str__(self) -> str:
        return f'{self.id} - {self.first_name} {self.last_name} - {self.organization.name}'


class OrganizationClient(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    allergies:str = models.TextField()

    birth_date:datetime.date = models.DateField()

    comments:str = models.TextField()

    emergency_contact:str = models.CharField(max_length=255)
    email:str = models.CharField(max_length=255)

    first_name:str = models.CharField(max_length=255)
    last_name:str = models.CharField(max_length=255)

    identification:str = models.CharField(max_length=255)

    phone:str = models.CharField(max_length=255)
    phone2:str = models.CharField(max_length=255)

    known_conditions:str = models.TextField()
    
    rating:int = models.IntegerField()
    referral_link:str = models.CharField(max_length=255)

    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:KumbioUser = models.ForeignKey(KumbioUser, on_delete=models.CASCADE, related_name='organization_client_created_by')
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_client_updated_by')
    deleted_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_client_deleted_by')

    # to get the appointment that this client had done, we have to call the calendar api

    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name} - {self.organization.name}'
    


# @receiver(post_delete, sender=KumbioUser)
# def after_delete_user(sender, instance:KumbioUser, using, **kwargs):
#     instance.organization.reduce_active_number_of_users()
    

# @receiver(post_save, sender=KumbioUser)
# def after_save_user(sender, instance:KumbioUser, created, **kwargs):
    
#     if created:
        
#         instance.organization.increment_active_number_of_users()

#         if instance.organization.active_number_of_users > instance.organization.plan.max_number_of_users:
#             instance.delete()
#             raise ValidationError("This organization has reached the maximum number of users allowed.")


