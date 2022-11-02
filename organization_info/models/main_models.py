# python
import secrets
import datetime
import os
from dotenv import load_dotenv

# django
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

# models
import user_info.models as user_models

# utils
from utils.integer_choices import RatingMadeBy


load_dotenv()

class Sector(models.Model):
    name:str = models.CharField(max_length=100)
    description:str = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class Organization(models.Model):
    
    # Foreign Keys -----------------------------------------------------------
    # plan:KumbioPlan = models.ForeignKey(KumbioPlan, on_delete=models.CASCADE, default=1)
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
    
    default_template_starts_at:int = models.IntegerField(default=0)
    
    # owner data

    owner_email:str = models.EmailField()
    owner_first_name:str = models.CharField(max_length=120)
    owner_last_name:str = models.CharField(max_length=120)
    owner_phone:str = models.CharField(max_length=120)

    # ------------------------------------------------------------------------
    # Logs -------------------------------------------------------------------
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetime_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)


    # Properties -------------------------------------------------------------
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
    

    # call a request to the calendar api to get the number of appoinments
    @property
    def number_of_appointments(self) -> int:
        return self.appointment_set.count()
    
    
    # methods
    def set_default_template_starts_at(self, starts_at:int) -> None:
        self.default_template_starts_at = starts_at
        self.save()
        
        
    # other methods    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.invitation_link = secrets.token_urlsafe(21)
            self.link_dashboard = secrets.token_urlsafe(21)
            self.id = secrets.token_urlsafe(21)
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

    # logs fields
    created_at:datetime.datetime = models.DateTimeField(default=datetime.datetime.utcnow)

    deleted_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='service_deleted_by')

    updated_at:datetime.datetime = models.DateTimeField(null=True, default=None)
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='service_updated_by')

        
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

    address:str = models.CharField(max_length=255)
    accepts_children:bool = models.BooleanField(default=True)
    accepts_pets:bool = models.BooleanField(default=True)
    additional_info:str = models.CharField(max_length=255, null=True, blank=True)

    email:str = models.EmailField(max_length=255, null=True, blank=True)

    name:str = models.CharField(max_length=255)

    phone:str = models.CharField(max_length=255, null=True, blank=True)

    opens_at = models.TimeField(default=datetime.time(8, 0, 0))
    closes_at = models.TimeField(default=datetime.time(18, 0, 0))

    photo:str = models.CharField(max_length=255, null=True, blank=True)
    
    local_timezone:str = models.CharField(max_length=120, default='America/Bogota')

    # -----------------------------------------------------------
    # Logs 
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organizaion_place_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='organizaion_place_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='organizaion_place_deleted_by')

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


class OrganizationProfessional(models.Model):

    # foreignkeys
    
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_professionals')
    kumbio_user:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='user_professional')
    
    specialities = models.ManyToManyField('ProfessionalSpeciality', blank=True)
    services = models.ManyToManyField(OrganizationService)
    
    # -----------------------------------------------------------
    # fields
    academic_formation:str = models.TextField(blank=True, null=True)
    about_me:str = models.TextField(blank=True, null=True)
    
    certificates = models.FileField(upload_to=f'{organization.name}/professionals/certificates/', null=True, blank=True)

    experience:str = models.TextField(blank=True, null=True)
    
    photos = models.FileField(upload_to=f'{organization.name}/professionals/photos/', null=True, blank=True)
    profile_photo = models.ImageField(upload_to=f'{organization.name}/professionals/profile_photos/', null=True, blank=True)
    
    
    # -----------------------------------------------------------
    # Logs 
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

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


class OrganizationClient(models.Model):
    # Foreignkeys
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # -----------------------------------------------------------
    
    
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

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organization_client_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_client_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_client_deleted_by')

    # to get the appointment that this client had done, we have to call the calendar api

    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name} - {self.organization.name}'
    

class OrganizationPromotion(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    service:OrganizationService = models.ForeignKey(OrganizationService, on_delete=models.CASCADE)
    
    name:str = models.CharField(max_length=255)
    description:str = models.TextField()
    discount:int = models.IntegerField()
    
    from_date:datetime.date = models.DateField()
    to_date:datetime.date = models.DateField(null=True, blank=True)
    
    photo = models.ImageField(upload_to=f'{organization.name}/promotions/photos/', null=True, blank=True)
    
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organization_promotion_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_promotion_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_promotion_deleted_by')

    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'


class OrganizationCampaings(models.Model):
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
    
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='organization_campaing_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_campaing_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='organization_campaing_deleted_by')

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
    
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

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
    
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='rating_deleted_by')

    created_by:int = models.IntegerField(choices=RatingMadeBy.choices)
    
    def __str__(self):
        return f'{self.id} - {self.client.first_name} {self.client.last_name} - {self.organization.name}'

 
class ProfessionalSpeciality(models.Model):
    organization:'Organization' = models.ForeignKey('Organization', on_delete=models.CASCADE)
    
    name:str = models.CharField(max_length=255)

    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='professional_speciality_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='professional_speciality_updated_by')
    
    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'


class FrequentlyAskedQuestion(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    service:OrganizationService = models.ForeignKey(OrganizationService, on_delete=models.CASCADE)
    professional:OrganizationProfessional = models.ForeignKey(OrganizationProfessional, on_delete=models.CASCADE)
    
    question:str = models.TextField()
    answer:str = models.TextField()
    
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='faq_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='faq_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='faq_deleted_by')

    def __str__(self):
        return f'{self.id} - {self.question[:20]} - {self.organization.name}'

