# python
import secrets
import datetime
import requests
import os
import sys
import json
from types import SimpleNamespace

from dotenv import load_dotenv

# django
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.validators import MaxValueValidator, MinValueValidator

# models
import user_info.models as user_models

# utils
from utils.integer_choices import RatingMadeBy

from print_pp.logging import Print
from organization_info.utils import get_start_and_end_time


load_dotenv()

KUMBIO_COMMUNICATIONS_ENDPOINT = os.getenv('KUMBIO_COMMUNICATIONS_ENDPOINT')

class Sector(models.Model):
    name:str = models.CharField(max_length=100)
    description:str = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class Organization(models.Model):
    
    # Foreign Keys -----------------------------------------------------------
    # plan:KumbioPlan = models.ForeignKey(KumbioPlan, on_delete=models.CASCADE, default=1)
    sector:Sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, default=None, blank=True)
    id:str = models.CharField(max_length=100, primary_key=True)
    
    email_templates:list = models.JSONField(default=list)
    
    # ------------------------------------------------------------------------
    # Fields -----------------------------------------------------------------

    # data
    
    cancellation_policy:str = models.TextField(null=True, blank=True)
    country:str = models.CharField(max_length=120, default='')
    currency:str = models.CharField(max_length=120, default='')
    
    data_policy:str = models.TextField(null=True, blank=True)
    description:str = models.CharField(max_length=120, default='')
    
    email:str = models.EmailField(unique=True)
    
    invitation_link:str = models.CharField(max_length=256, unique=True, null=True, default=None)
    
    link_dashboard:str = models.CharField(max_length=120, null=True, blank=True)
    logo = models.ImageField(upload_to='organization_logos', null=True, blank=True)
    language:str = models.CharField(max_length=120, default='')
    
    name:str = models.CharField(max_length=120, unique=True)
    notification_email:str = models.EmailField(default=os.environ['DEFAULT_EMAIL'])
    notification_email_password = models.BinaryField(default=os.environ['DEFAULT_EMAIL_PASSWORD'].encode())

    phone:str = models.CharField(max_length=120)
    
    rating:float = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    website:str = models.CharField(max_length=120, null=True, blank=True)
    
    template_to_send_as_confirmation:int = models.IntegerField(default=0)
    template_to_send_as_reminder_1:int = models.IntegerField(default=0)
    template_to_send_as_reminder_2:int = models.IntegerField(default=0)
    template_to_send_as_rescheduled:int = models.IntegerField(default=0)
    template_to_send_as_canceled:int = models.IntegerField(default=0)
    template_to_send_as_new_client_to_calendar_user:int = models.IntegerField(default=0)
    template_to_send_as_rescheduled_to_calendar_user:int = models.IntegerField(default=0)
    template_to_send_as_canceled_to_calendar_user:int = models.IntegerField(default=0)
    
    # owner data
    owner_email:str = models.EmailField()
    owner_first_name:str = models.CharField(max_length=120)
    owner_last_name:str = models.CharField(max_length=120)
    owner_phone:str = models.CharField(max_length=120)

    # ------------------------------------------------------------------------
    # Logs -------------------------------------------------------------------
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)


    # Properties -------------------------------------------------------------
    @property
    def owner(self) -> user_models.KumbioUser:
        return user_models.KumbioUser.objects.get(email=self.owner_email)
    
    @property
    def services(self) -> QuerySet:
        return self.organizationservice.all()       
    
    @property
    def professionals(self) -> QuerySet['OrganizationProfessional']:
        return self.organizationprofessional.all()
    
    
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
    

    # call a request to the calendar api to get the number of appointments
    @property
    def number_of_appointments(self) -> int:
        return self.appointment_set.count()
            
        
    # other methods    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.invitation_link = secrets.token_urlsafe(21)
            self.link_dashboard = secrets.token_urlsafe(21)
            self.id = secrets.token_urlsafe(21)
            
            if not 'test' in sys.argv:
                res = requests.post(
                    f'{KUMBIO_COMMUNICATIONS_ENDPOINT}message-templates/mail-templates/',
                    headers={'Authorization': os.environ["TOKEN_FOR_CALENDAR"]},
                    json={
                        'organization_id': self.id,
                        'created_by': 0, # id 0 is for owner of the organization
                        'use_default_templates': True
                    })
                
                Print('res', res.json())
            
                for template_id in res.json()['template_ids']:
                    self.email_templates.append(template_id)
                        
        super().save(*args, **kwargs)
                
        
    def __str__(self) -> str:
        return f'{self.id} - {self.name} - {self.email}'


class OrganizationService(models.Model):
    
    # ---------------------------------------------------------------
    # Foreign Keys
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, default=None)
    # ---------------------------------------------------------------
    # Fields
    
    service:str = models.CharField(max_length=100)

    description:str = models.TextField(blank=True, null=True)

    time_interval:float = models.FloatField(default=1)
    
    price:float = models.FloatField(default=0)

    # logs fields
    created_at:datetime.datetime = models.DateTimeField(default=datetime.datetime.utcnow)

    deleted_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='service_deleted_by')

    updated_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='service_updated_by')

        
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
    

    @property
    def is_updated(self) -> bool:
        return self.updated_at is not None


    def set_updated_by(self, user:user_models.KumbioUser):
        self.updated_by = user
        self.save()


    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.datetime.utcnow()
        else:
            self.updated_at = datetime.datetime.utcnow()
                    
        super().save(*args, **kwargs)
    
    
    def delete(self, *args, **kwargs):
        self.deleted_at = datetime.datetime.utcnow()
        self.deleted_by = kwargs.get('user')
        self.save()
    
    
    def __str__(self) -> str:
        return f'{self.id} {self.organization.name} - {self.service}'


class OrganizationPlace(models.Model):
    # foreignkeys
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    payment_methods_accepted = models.ManyToManyField('PaymentMethodAcceptedByOrg', blank=True)
    services = models.ManyToManyField(OrganizationService, blank=True)
    
    # fields

    address:str = models.CharField(max_length=255, null=True, default=None, blank=True)
    admin_email:str = models.CharField(max_length=255, null=True, default=None, blank=True)
    accepts_children:bool = models.BooleanField(default=True)
    accepts_pets:bool = models.BooleanField(default=True)
    additional_info:str = models.CharField(max_length=255, null=True, default=None, blank=True)
    after_hours_phone:str = models.CharField(max_length=255, null=True, default=None, blank=True)

    email:str = models.EmailField(max_length=255, null=True, default=None, blank=True)

    google_maps_link:str = models.CharField(max_length=255, null=True, default=None, blank=True)

    important_information:str = models.TextField(null=True, default=None, blank=True)

    main_office_number:str = models.CharField(max_length=255, null=True, default=None, blank=True)

    name:str = models.CharField(max_length=255)

    phone:str = models.CharField(max_length=255, null=True, default=None, blank=True)

    photo:str = models.CharField(max_length=255, null=True, default=None, blank=True)
    
    local_timezone:str = models.CharField(max_length=120, default='', blank=True)
    
    # if this place has a custom price for a service
    custom_price:list[dict] = models.JSONField(default=list, null=True, blank=True)
    
    """ 
        custom_price = [{
            place_id: 1,
            price: 25,
        }]
    """

    # -----------------------------------------------------------
    # Logs 
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organization_place_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='organization_place_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='organization_place_deleted_by')

    # -----------------------------------------------------------
    # Properties

    # -----------------------------------------------------------
    # Methods

    def save(self, *args, **kwargs):
        first_time = False
        if not self.pk:
            first_time = True
            
        super().save(*args, **kwargs)
        
        if first_time:
            if not self.payment_methods_accepted:
                self.payment_methods.add(*self.organization.payment_methods_accepted.all())
    
    
    def __str__(self):
        return f'{self.name} - {self.organization.name}'


class DayName(models.IntegerChoices):
    MONDAY = 0, 'Monday'
    TUESDAY = 1, 'Tuesday'
    WEDNESDAY = 2, 'Wednesday'
    THURSDAY = 3, 'Thursday'
    FRIDAY = 4, 'Friday'
    SATURDAY = 5, 'Saturday'
    SUNDAY = 6, 'Sunday'


class DayAvailableForPlace(models.Model):

    place:OrganizationPlace = models.ForeignKey(OrganizationPlace, on_delete=models.CASCADE)
    
    week_day:int = models.IntegerField(choices=DayName.choices)
    exclude:list = models.JSONField(default=list, null=True, blank=True)

    note:str = models.TextField(null=True, blank=True)

    @property
    def opens_at(self) -> str:
        return get_start_and_end_time(self.exclude)[0]
    

    @property
    def closes_at(self) -> str:
        return get_start_and_end_time(self.exclude)[1]

    
    @property
    def day_name(self) -> str:
        return DayName(self.week_day).label


    def save(self, *args, **kwargs):
        if not self.pk and not self.exclude:
            self.exclude = [[0, 7], [18, 23]]
                    
        super().save(*args, **kwargs)


class OrganizationProfessional(models.Model):

    # foreignkeys
    
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_professionals')
    kumbio_user:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='user_professional')
    
    specialties = models.ManyToManyField('ProfessionalSpecialty', blank=True)
    services = models.ManyToManyField(OrganizationService)
    
    # -----------------------------------------------------------
    # fields
    academic_formation:str = models.TextField(blank=True, null=True)
    about_me:str = models.TextField(blank=True, null=True)
    
    certificates = models.FileField(upload_to=f'{organization.name}/professionals/certificates/', null=True, blank=True)

    experience:str = models.TextField(blank=True, null=True)
    
    photos = models.FileField(upload_to=f'{organization.name}/professionals/photos/', null=True, blank=True)
    profile_photo = models.ImageField(upload_to=f'{organization.name}/professionals/profile_photos/', null=True, blank=True)
    
    # if this professional has a custom price for a service
    custom_price:list[dict] = models.JSONField(default=list)
    
    """
        custom_price = [{
            place_id: 1,
            price: 25,
        }]
    """
    
    # -----------------------------------------------------------
    # Logs 
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='professional_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_deleted_by')
    
    # -----------------------------------------------------------
    # properties
    
    @property
    def services(self) -> QuerySet:
        return self.organizationservice.all()
    
    @property
    def number_of_services(self) -> int:
        return self.services.count()


    @property
    def full_name(self) -> str:
        return f'{self.kumbio_user.first_name} {self.kumbio_user.last_name}'
    
    # -----------------------------------------------------------
    # methods
        
    def __str__(self) -> str:
        return f'{self.id} - {self.kumbio_user.first_name} {self.kumbio_user.last_name} - {self.organization.name}'


class OrganizationClientType(models.Model):
    
        organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_client_types')
        name:str = models.CharField(max_length=100)
        description:str = models.TextField(blank=True, null=True, default='')

        fields:dict = models.JSONField()

        # Fields is going to be a JSON object where the person is going to be able to save as many fields as the want
        # this way, we can assure that we can save any kind of information that the client wants to save    
        # -----------------------------------------------------------
        # Logs 
        created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
        updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
        deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    
        created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='client_type_created_by')
        updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='client_type_updated_by')
        deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='client_type_deleted_by')
        
        # -----------------------------------------------------------
        # properties

        @property
        def fields_available(self) -> list:
            return list(self.fields.keys())
        
        # -----------------------------------------------------------
        # methods

        def convert_fields_to_object(self) -> object:
            return json.loads(self.fields, object_hook=lambda d: SimpleNamespace(**d))

        
        def save(self, *args, **kwargs):

            if not self.pk and not self.created_by:
                self.created_by = user_models.KumbioUser.objects.get(pk=kwargs.get('created_by'))

            super().save(*args, **kwargs)
            
            
        def __str__(self) -> str:
            return f'{self.pk} - {self.name} - {self.organization.name}'


class OrganizationClientCreatedBy(models.IntegerChoices):
    CALENDAR = 1
    ORDERS = 2
    KUMBIO = 3
    COMMUNICATIONS = 4
    

class OrganizationClient(models.Model):
    # Foreignkeys
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    type:OrganizationClientType = models.ForeignKey(OrganizationClientType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # -----------------------------------------------------------
    
    birth_date:datetime.date = models.DateField(null=True, blank=True, default=None)

    comments:str = models.TextField(null=True, blank=True, default=None)

    emergency_contact:str = models.CharField(max_length=255, null=True, blank=True, default=None)

    first_name:str = models.CharField(max_length=255)
    last_name:str = models.CharField(max_length=255)

    identification:str = models.CharField(max_length=255, null=True, blank=True, default=None)

    birthday:datetime.date = models.DateField(null=True, blank=True, default=None)
    age:int = models.IntegerField(null=True, blank=True, default=None)

    rating:int = models.IntegerField(null=True, blank=True, default=None, validators=[MinValueValidator(10), MaxValueValidator(100)])
    referral_link:str = models.CharField(max_length=255)

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:int = models.IntegerField(choices=OrganizationClientCreatedBy.choices, default=OrganizationClientCreatedBy.CALENDAR)
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_client_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_client_deleted_by')

    # to get the appointment that this client had done, we have to call the calendar api

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    

    @property
    def dependent(self):
        return self.organizationclientdependent_set.all()[0]

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.referral_link = secrets.token_urlsafe(16)

        super().save(*args, **kwargs)

    
    def __str__(self):
        return f'{self.id} - {self.full_name} - {self.organization.name}'
    

class OrganizationClientDependent(models.Model):

    # foreignkeys
    client:OrganizationClient = models.ForeignKey(OrganizationClient, on_delete=models.CASCADE, related_name='client_dependent')

    first_name:str = models.CharField(max_length=100)
    last_name:str = models.CharField(max_length=100)
    email:str = models.EmailField()
    phone:str = models.CharField(max_length=20)
    phone_2:str = models.CharField(max_length=20, blank=True, null=True, default=None)

    same_as_client:bool = models.BooleanField(default=True)
    
    # -----------------------------------------------------------


class OrganizationPromotion(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    service:OrganizationService = models.ForeignKey(OrganizationService, on_delete=models.CASCADE)
    
    name:str = models.CharField(max_length=255)
    description:str = models.TextField()
    discount:int = models.IntegerField()
    
    from_date:datetime.date = models.DateField()
    to_date:datetime.date = models.DateField(null=True, blank=True)
    
    photo = models.ImageField(upload_to=f'{organization.name}/promotions/photos/', null=True, blank=True)
    
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organization_promotion_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_promotion_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_promotion_deleted_by')

    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'


class OrganizationCampaigns(models.Model):
    # Foreignkeys
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # -----------------------------------------------------------
    
    name:str = models.CharField(max_length=255)
    description:str = models.TextField()
    
    token:str = models.CharField(max_length=255)
    
    is_active:bool = models.BooleanField(default=False)
    budget:int = models.IntegerField()
    
    from_date:datetime.date = models.DateField()
    to_date:datetime.date = models.DateField(null=True, blank=True)
    
    photo = models.ImageField(upload_to=f'{organization.name}/promotions/photos/', null=True, blank=True)
    
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organization_campaign_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_campaign_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_campaign_deleted_by')

    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'


class OrganizationProduct(models.Model):
    
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    name:str = models.CharField(max_length=255)
    description:str = models.TextField()
    
    price:int = models.IntegerField()
    
    photo = models.ImageField(upload_to=f'{organization.name}/products/photos/', null=True, blank=True)
    
    is_available:bool = models.BooleanField(default=True)
    amount:int = models.IntegerField()
    
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organization_product_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_product_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_product_deleted_by')

    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'
 
 
class Rating(models.Model):
    client:OrganizationClient = models.ForeignKey(OrganizationClient, on_delete=models.CASCADE, related_name='client')
    service:OrganizationService = models.ForeignKey(OrganizationService, on_delete=models.CASCADE)
    Professional:OrganizationProfessional = models.ForeignKey(OrganizationProfessional, on_delete=models.CASCADE, related_name='professional')
    
    rating:int = models.IntegerField()
    comment:str = models.TextField()
    
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='rating_deleted_by')

    created_by:int = models.IntegerField(choices=RatingMadeBy.choices)
    
    def __str__(self):
        return f'{self.id} - {self.client.first_name} {self.client.last_name} - {self.organization.name}'

 
class ProfessionalSpecialty(models.Model):
    organization:'Organization' = models.ForeignKey('Organization', on_delete=models.CASCADE)
    
    name:str = models.CharField(max_length=255)

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='professional_specialty_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='professional_specialty_updated_by')
    
    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'


class FrequentlyAskedQuestion(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    service:OrganizationService = models.ForeignKey(OrganizationService, on_delete=models.CASCADE)
    professional:OrganizationProfessional = models.ForeignKey(OrganizationProfessional, on_delete=models.CASCADE)
    
    question:str = models.TextField()
    answer:str = models.TextField()
    
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='faq_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='faq_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='faq_deleted_by')

    def __str__(self):
        return f'{self.id} - {self.question[:20]} - {self.organization.name}'

