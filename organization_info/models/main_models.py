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
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


# rest_framework
from rest_framework import exceptions

# models
import user_info.models as user_models
from .default_values import DEFAULT_CLIENT_TYPES


# utils
from utils.integer_choices import RatingMadeBy
from organization_info.utils.time import get_start_and_end_time
from organization_info.utils.enums import DayName, OrganizationClientCreatedBy
from .payment_models import PaymentMethodAcceptedByOrg

from kumbio_communications import send_notification

from print_pp.logging import Print


load_dotenv()

KUMBIO_COMMUNICATIONS_ENDPOINT = os.getenv('KUMBIO_COMMUNICATIONS_ENDPOINT')
SELF_CALENDAR_USER = os.getenv('SELF_CALENDAR_USER')
TOKEN_FOR_CALENDAR = os.getenv('TOKEN_FOR_CALENDAR')
COMMUNICATIONS_TOKEN = os.getenv('COMMUNICATIONS_TOKEN')
CALENDAR_ENDPOINT = os.getenv('CALENDAR_ENDPOINT')


class Sector(models.Model):
    name:str = models.CharField(max_length=100)
    spanish_name:str = models.CharField(max_length=100, default=None, null=True, blank=True)
    description:str = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class OrganizationClientType(models.Model):

    """
        When a new organization is created, it will be a list of default client types that will be created
        along with the organization. This way, with each organization with its own client types, it will be
        possible for the organization to create new client types, edit and delete them.
    """

    organization:'Organization' = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='organization_client_type')
    sector:Sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='sector', default=None, null=True)

    name:str = models.CharField(max_length=100)
    description:str = models.TextField(blank=True, null=True, default='')

    fields:list[tuple] = models.JSONField(default=list)

    """
        fields is going to be a JSON object where the person is going to be able to save as many fields 
        as they want; this way we can assure that we can save any kind of information that the client
        wants to save

        the way this information is saved, is with a list of tuples, where the first element is the name
        and the second element is the type of the field

        example:

        fields = [('name', FieldType.TEXT), ('age', FieldType.NUMBER)]

        where, for the moment, there are just two types of fields: text and number

        we can also place a third element in the tuple, which can be a validator for the field
        where some settings can be set, like the minimum and maximum length of the text, or the minimum
        and maximum value of the number. Also to check more specific things, like if the number is
        positive or negative, or if the text is a valid email, or if the number is a valid phone number.
    """
    # -----------------------------------------------------------
    # Logs 
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='client_type_created_by')
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
            try: self.created_by = user_models.KumbioUser.objects.get(pk=kwargs.get('created_by'))
            except user_models.KumbioUser.DoesNotExist: pass 
            # this pass is here because if the user is not specified, it will mean
            # that the user is the one that is creating the organization, and that
            # user will be the one that is creating the client type      

        super().save(*args, **kwargs)
        
        
    def __str__(self) -> str:
        return f'{self.pk} - {self.name} - {self.organization.name}'


class Organization(models.Model):
    
    # Foreign Keys -----------------------------------------------------------
    # plan:KumbioPlan = models.ForeignKey(KumbioPlan, on_delete=models.CASCADE, default=1)
    id:str = models.CharField(max_length=100, primary_key=True)
    
    sector:Sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, default=None, blank=True)
    payment_methods_accepted = models.ManyToManyField(PaymentMethodAcceptedByOrg, blank=True, related_name='payment_methods_accepted_by_org')
    
    email_templates:list = models.JSONField(default=list)
    
    # ------------------------------------------------------------------------
    # Fields -----------------------------------------------------------------

    # data

    about_us_image = models.ImageField(upload_to='about_us', null=True, blank=True, default=None)
    
    cancellation_policy:str = models.TextField(null=True, blank=True)
    country:str = models.CharField(max_length=120, default='')
    currency:str = models.CharField(max_length=120, default=None, null=True, blank=True)
    
    data_policy:str = models.TextField(null=True, blank=True)
    description:str = models.CharField(max_length=120, default=None, null=True, blank=True)
    default_timezone:str = models.CharField(max_length=120, default='America/Caracas', null=True, blank=True)
    default_client_type:int = models.IntegerField(default=5)

    email:str = models.EmailField(unique=True)
    
    invitation_link:str = models.CharField(max_length=256, unique=True, null=True, default=None)
    
    link_dashboard:str = models.CharField(max_length=120, null=True, blank=True)
    logo = models.ImageField(upload_to='organization_logos', null=True, blank=True, default=None)
    language:str = models.CharField(max_length=120, default=None, null=True, blank=True)
    
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


    # ------------------------------------------------------------------------
    # Organization related information
    number_of_professionals:int = models.IntegerField(default=0)
    number_of_clients:int = models.IntegerField(default=0)
    number_of_services:int = models.IntegerField(default=0)
    number_of_appointments:int = models.IntegerField(default=0)
    number_of_active_appointments:int = models.IntegerField(default=0)


    # Properties -------------------------------------------------------------
    @property
    def owner(self) -> user_models.KumbioUser:
        return user_models.KumbioUser.objects.get(email=self.owner_email)
    

    @property
    def services(self) -> QuerySet['OrganizationService']:
        return self.organizationservice.all()
    

    @property
    def professionals(self) -> QuerySet['OrganizationProfessional']:
        return self.organization_professionals.all()

    
    @property
    def client_types(self) -> QuerySet['OrganizationClientType']:
        return self.organization_client_type.all()
    

    @property
    def most_used_service(self) -> tuple['OrganizationService', int]:
        most_used = None

        for service in self.services:
            if most_used is None:
                most_used = service
            else:
                if service.number_of_appointments > most_used.number_of_appointments:
                    most_used = service

        return most_used, most_used.number_of_appointments


    # TODO: this must come from calendar api
    @property
    def calendars(self) -> QuerySet:
        # perform a query to get all calendars to the calendar api
        return self.calendar_set.all()
    

    # Methods --------------------------------------------------------------

    def increment_number_of_professionals(self):
        self.number_of_professionals += 1
        self.save()

    
    def increment_number_of_clients(self):
        self.number_of_clients += 1
        self.save()

    
    def increment_number_of_active_appointments(self):
        self.number_of_active_appointments += 1
        self.increment_number_of_appointments()

    
    def increment_number_of_appointments(self):
        self.number_of_appointments += 1
        self.save()

        
    def increment_number_of_services(self):
        self.number_of_services += 1
        self.save()

    
    def decrement_number_of_professionals(self):
        self.number_of_professionals -= 1
        self.save()
    

    def decrement_number_of_clients(self):
        self.number_of_clients -= 1
        self.save()

    
    def decrement_number_of_services(self):
        self.number_of_services -= 1
        self.save()
    

    def decrement_number_of_appointments(self):
        self.number_of_appointments -= 1
        self.save()
    

    def get_number_of_professionals(self) -> int:
        return self.professionals.count()

    
    def get_number_of_services(self) -> int:
        return self.services.count()
    

    def get_number_of_calendars(self) -> int:
        # TODO call a request to the calendar api to get the number of calendars
        raise NotImplementedError('This method is not implemented yet')   

    # call a request to the calendar api to get the number of appointments
    
    def get_number_of_appointments(self) -> int:
        # TODO call a request to the calendar api to get the number of calendars
        raise NotImplementedError('This method is not implemented yet')
    

    def set_default_client_type(self, client_type: 'OrganizationClientType'):
        self.default_client_type = client_type.pk
        self.save()
        

    # other methods    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.invitation_link = secrets.token_urlsafe(21)
            self.link_dashboard = secrets.token_urlsafe(21)
            self.id = secrets.token_urlsafe(21)
            super().save(*args, **kwargs)

            # we need to create the default client_types for this organization
            # we need to create the default client_types for this organization
            client_fields = DEFAULT_CLIENT_TYPES[int(self.sector.pk) - 1]
            client_type = OrganizationClientType.objects.create(
                organization=self, 
                name=client_fields['name'], 
                description=client_fields['description'], 
                fields=client_fields['fields'],
                created_by=None)
            self.set_default_client_type(client_type)
            
            
            if not 'test' in sys.argv:
                res = requests.post(
                    f'{KUMBIO_COMMUNICATIONS_ENDPOINT}message-templates/mail-templates/',
                    headers={'Authorization': os.environ["TOKEN_FOR_CALENDAR"]},
                    json={
                        'organization_id': self.id,
                        'created_by': 0, # id 0 is for owner of the organization when the organization is being created
                        'use_default_templates': True
                    })
            
                for template_id in res.json()['template_ids']:
                    self.email_templates.append(template_id)
        else:
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
    conditions_and_discounts:str = models.TextField(blank=True, null=True)

    time_interval:float = models.FloatField(default=1)
    
    price:float = models.FloatField(default=0)

    buffer:float = models.FloatField(default=0)
    online_booking:int = models.BooleanField(default=True)

    # logs fields
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)

    deleted_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='service_deleted_by')

    updated_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='service_updated_by')


    number_of_appointments:int = models.IntegerField(default=0)
    number_of_active_appointments:int = models.IntegerField(default=0)
        

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
    

    @property
    def is_updated(self) -> bool:
        return self.updated_at is not None
    

    # ---------------------------------------------------------------
    # Methods

    def increment_number_of_active_appointments(self):
        self.number_of_active_appointments += 1
        self.increment_number_of_appointments()


    def increment_number_of_appointments(self):
        self.number_of_appointments += 1
        self.save()


    def set_updated_by(self, user:user_models.KumbioUser):
        self.updated_by = user
        self.save()


    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
                    
        super().save(*args, **kwargs)
    
    
    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
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

    description:str = models.TextField(null=True, default=None, blank=True)

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

    @property
    def available_days(self) -> QuerySet['DayAvailableForPlace']:
        return self.dayavailableforplace_set.all()

    # -----------------------------------------------------------
    # Methods

    def get_day_available(self, week_day:DayName) -> 'DayAvailableForPlace | None':
        try:
            return self.available_days.get(week_day=week_day)
        except DayAvailableForPlace.DoesNotExist:
            return None


    def save(self, *args, **kwargs):
        first_time = False
        if not self.pk:
            first_time = True
        else:
            self.updated_at = timezone.now()

        super().save(*args, **kwargs)
        
        if first_time:
            if not self.payment_methods_accepted:
                self.payment_methods_accepted.add(*self.organization.payment_methods_accepted.all())
        
    
    def __str__(self):
        return f'{self.name} - {self.organization.name}'


class DayAvailableForPlace(models.Model):

    place:OrganizationPlace = models.ForeignKey(OrganizationPlace, on_delete=models.CASCADE)
    
    week_day:int = models.IntegerField(choices=DayName.choices)
    exclude:list = models.JSONField(default=list, null=True, blank=True)

    note:str = models.TextField(null=True, blank=True)

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)


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
        else:
            self.updated_at = timezone.now()
                    
        super().save(*args, **kwargs)


class DayAvailableForProfessional(models.Model):
    
    professional:'OrganizationProfessional' = models.ForeignKey('OrganizationProfessional', on_delete=models.CASCADE)
    
    week_day:int = models.IntegerField(choices=DayName.choices)
    exclude:list = models.JSONField(default=list, null=True, blank=True)

    services:dict = models.JSONField(default=dict, null=True, blank=True)

    """
        services = {
            int['service_id']: {
                'time_interval': 1,
            },
            int['service_id']: {
                'time_interval': 0.5,
            },
            int['service_id']: {
                'time_interval': .25,
            },
        }
    """
   

    note:str = models.TextField(null=True, blank=True)


    @property
    def day_name(self) -> str:
        return DayName(self.week_day).label

    
    def get_start_and_end_time_for_service(self, service_id:int) -> tuple:
        return get_start_and_end_time(self.exclude)
    

    def delete_service(self, service_id:str|int) -> bool:
        """
            Returns True if the service was deleted and False if the service was not found
        """
        if not isinstance(service_id, str) and not isinstance(service_id, int):
            raise TypeError(f'Expected str or int, got {type(service_id)}')

        
        if isinstance(service_id, int):
            service_id = f'#{service_id}'
        
        
        if '#' not in service_id:
            service_id = f'#{service_id}'

        
        services = self.services
        
        try: services.pop(str(service_id))
        except KeyError: return False
        
        self.services = services
        self.save()
        
        return True


    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.exclude:
                self.exclude = [[0, 7], [18, 23]]
            self.__add_day_to_calendar()
        else:
            self.__update_days_on_calendar_api()
                    
        super().save(*args, **kwargs)

    
    def __add_day_to_calendar(self):
        data = {
            'calendar_link': self.professional.kumbio_user.calendar_link,
            'days': [{
                'week_day': self.week_day,
                'exclude': self.exclude,
                'services': self.services,
            }]
        }
        res = requests.post(
            f'{CALENDAR_ENDPOINT}calendar/api/v2/day-available-for-professional/', 
            headers={'authorization': 'Token ' + self.professional.kumbio_user.calendar_token}, 
            json=data
        )
        if res.status_code != 201:
            Print(res.json())
            raise exceptions.APIException(res.json())
        

    def __update_days_on_calendar_api(self):
        """
        Actualiza los días disponibles en el calendario.

        Parameters:
        - day_available (DayAvailable): Instancia del día disponible.
        """

        data = {
            'calendar_link': self.professional.kumbio_user.calendar_link,
            'days': [{
                'week_day': self.week_day,
                'exclude': self.exclude,
                'services': self.services
            }]
        }

        res = requests.put(
            f'{CALENDAR_ENDPOINT}calendar/api/v2/day-available-for-professional/', 
            headers={'authorization':f'Token {self.professional.kumbio_user.calendar_token}'},
            json=data
        )
        
        if res.status_code != 200:
            try: raise exceptions.ValidationError(_(res.json()))
            except: raise exceptions.APIException(_('error in calendar api'))
    

    def __delete_days_on_calendar_api(self):
        """
        Elimina los días disponibles en el calendario.

        Parameters:
        - day_available (DayAvailable): Instancia del día disponible.
        """
        
        data = {
            'calendar_link': self.professional.kumbio_user.calendar_link,
            'week_days': [self.week_day]
        }

        res = requests.delete(
            f'{CALENDAR_ENDPOINT}calendar/api/v2/day-available-for-professional/',
            headers={'authorization': f'Token {self.professional.kumbio_user.calendar_token}'},
            json=data
        )

        if res.status_code != 204:
            try: raise exceptions.ValidationError(_(res.json()))
            except: raise exceptions.APIException(_('error in calendar api'))


    def delete(self, *args, **kwargs):
        self.__delete_days_on_calendar_api()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f'{self.professional.pk} - {self.day_name} - {self.professional.full_name}'
    

class OrganizationProfessional(models.Model):

    # foreignkeys
    
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_professionals')
    kumbio_user:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='user_professional')
    
    specialties = models.ManyToManyField('ProfessionalSpecialty', blank=True)
    services = models.ManyToManyField(OrganizationService)

    place:OrganizationPlace = models.ForeignKey(OrganizationPlace, on_delete=models.CASCADE, null=True, blank=True, default=None)
    
    # -----------------------------------------------------------
    # fields
    academic_formation:str = models.TextField(blank=True, null=True)
    about_me:str = models.TextField(blank=True, null=True)

    identification_number:str = models.TextField(blank=True, null=True, default=None)

    certification_number:str = models.TextField(blank=True, null=True, default=None)
    charge:str = models.TextField(blank=True, null=True, default=None)
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
    def services_available(self) -> QuerySet:
        return self.organizationservice.all()
    
    @property
    def number_of_services(self) -> int:
        return self.services.count()


    @property
    def full_name(self) -> str:
        return f'{self.kumbio_user.first_name} {self.kumbio_user.last_name}'

    
    @property
    def available_days(self) -> QuerySet['DayAvailableForProfessional']:
        return self.dayavailableforprofessional_set.all()

    # -----------------------------------------------------------
    # Methods

    def get_day_available(self, week_day:DayName) -> 'DayAvailableForProfessional | None':
        try:
            return self.available_days.get(week_day=week_day)
        except DayAvailableForProfessional.DoesNotExist:
            return None

    
    def save(self, *args, **kwargs):
        first_time = False
        if not self.pk:
            first_time = True
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
                    
        super().save(*args, **kwargs)

        if first_time:
            self.__set_default_days_available()
            self.__send_welcome_message()
            self.save()
    

    # -----------------------------------------------------------
    # private methods

    # why is this commented out?
    def __set_default_days_available(self):
        return
        days_available = self.place.available_days
        for day in days_available:
            DayAvailableForProfessional.objects.create(
                professional=self,
                week_day=day.week_day,
                exclude=day.exclude,
                note=day.note
            )


    def __send_welcome_message(self):
        if 'test' in sys.argv or os.environ.get('FILLING_DB'): return

        send_notification(token_for_app=COMMUNICATIONS_TOKEN, 
                          organization_id=self.organization.id,
                          send_to=[self.kumbio_user.email],
                          messages=[f'Welcome to {self.organization.name}'],
                          subjects=['Welcome to kumbio'])

    
    def __str__(self) -> str:
        return f'{self.pk} - {self.kumbio_user.first_name} {self.kumbio_user.last_name} - {self.organization.name}'


class ClientParent(models.Model):

    # foreignkeys
    # At some moment im going to regret doing null=True, default=None but for now it is ok
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, default=None)

    first_name:str = models.CharField(max_length=100)
    last_name:str = models.CharField(max_length=100)
    email:str = models.CharField(max_length=255, blank=True, null=True, default=None)
    phone:str = models.CharField(max_length=50)
    phone_2:str = models.CharField(max_length=50, blank=True, null=True, default=None)
    address:str = models.CharField(max_length=255, blank=True, null=True, default=None)

    identification:str = models.CharField(max_length=255, null=True, blank=True, default=None)

    emergency_contact:str = models.CharField(max_length=255, null=True, blank=True, default=None)

    same_as_client:bool = models.BooleanField(default=True)

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)


    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'


    @property
    def children(self) -> QuerySet['OrganizationClient']:
        return self.client_child.all()

    
    def __str__(self) -> str:
        return f'{self.pk} - {self.full_name}'


class OrganizationClient(models.Model):
    # TODO: add professional fields to the client
    # TODO: Create referral_by field
    
    # Send these fields to the extra fields property
    # birthday:datetime.date = models.DateField(null=True, blank=True, default=None)
    # age:int = models.IntegerField(default=0)
    
    client_parent:ClientParent = models.ForeignKey(ClientParent, on_delete=models.CASCADE, default=None, null=True, related_name='client_child')
    type:OrganizationClientType = models.ForeignKey(OrganizationClientType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # -----------------------------------------------------------

    extra_fields:list = models.JSONField(default=list, null=False)

    """
        extra_fields is going to be a JSON coming from the type of client that was selected when creating
        the client. Making it possible to save any kind of information that the organization wants to save

        the way this information is saved, is with a list of tuples, where the first element is the name of the field
        and the second element is the type of the field, and the third element if the value of the field

        example:

        extra_fields = [('pets_first_name', FieldType.TEXT, 'first_name'), ('pets_last_name', FieldType.TEXT, 'last_name')]

        where, for the moment, there are just two types of fields: text and number

        we can also place a fourth element in the tuple, which can be a validator for the field
        where some settings can be set, like the minimum and maximum length of the text, or the minimum
        and maximum value of the number. Also to check more specific things, like if the number is
        positive or negative, or if the text is a valid email, or if the number is a valid phone number.
    """

    comments:str = models.TextField(null=True, blank=True, default=None)

    rating:int = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    referral_link:str = models.CharField(max_length=255)

    first_name:str = models.CharField(max_length=100, default='first_name')
    last_name:str = models.CharField(max_length=100, default='last_name')
    

    # notifications information
    # general notifications
    send_notifications_by_email:bool = models.BooleanField(default=True)
    send_notifications_by_sms:bool = models.BooleanField(default=True)
    send_notifications_by_whatsapp:bool = models.BooleanField(default=True)

    # marketing information
    send_marketing_by_email:bool = models.BooleanField(default=True)
    send_marketing_by_sms:bool = models.BooleanField(default=True)
    send_marketing_by_whatsapp:bool = models.BooleanField(default=True)

    # -----------------------------------------------------------
    # logs information

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)


    created_by_app:int = models.IntegerField(choices=OrganizationClientCreatedBy.choices, default=OrganizationClientCreatedBy.CALENDAR)
    created_by_user:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, blank=True, related_name='organization_client_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, blank=True, related_name='organization_client_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, blank=True, related_name='organization_client_deleted_by')

    # to get the appointment that this client had done, we have to call the calendar api

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
        
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.referral_link = secrets.token_urlsafe(16)

        super().save(*args, **kwargs)

    
    def __str__(self):
        return f'{self.pk} - {self.full_name} - {self.client_parent}'
    

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
        return f'{self.pk} - {self.name} - {self.organization.name}'


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
        return f'{self.id} - {self.client.first_name} {self.client.last_name}'

 
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
