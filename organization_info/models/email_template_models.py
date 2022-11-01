import datetime
from django.db import models
from django.utils import timezone

from user_info.models import KumbioUser
from .main_models import Organization


class TemplateTypes(models.IntegerChoices):
    CONFIRMATION_EMAIL = 0, 'Confirmation Email'
    REMINDER_EMAIL_1 = 1, 'Reminder Email 1'
    REMINDER_EMAIL_2 = 2, 'Reminder Email 2'
    REMINDER_EMAIL_3 = 3, 'Reminder Email 3'
    RESCHEDULED_EMAIL = 4, 'Rescheduled Email'
    CANCELED_EMAIL = 5, 'Canceled Email'
    NEW_CLIENT_TO_CALENDAR_USER = 6, 'New Client to Calendar User'
    RESCHEDULED_TO_CALENDAR_USER = 7, 'Rescheduled to Calendar User'
    CANCELED_TO_CALENDAR_USER = 8, 'Canceled to Calendar User'


class MailTemplate(models.Model):

    organization:Organization = models.ForeignKey(Organization, null=True, default=None, on_delete=models.CASCADE)

    name:str = models.CharField(max_length=120)
    subject:str = models.CharField(max_length=255)
    message:str = models.TextField()
    created_at:datetime.datetime = models.DateTimeField()
    updated_at:datetime.datetime = models.DateTimeField(null=True, default=None)

    template_type:int = models.IntegerField(null=True, choices=TemplateTypes.choices, default=None)

    # logs fields
    created_at:datetime.datetime = models.DateTimeField(default=datetime.datetime.utcnow)

    deleted_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='template_deleted_by')

    updated_at:datetime.datetime = models.DateTimeField(null=True, default=None)
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='template_updated_by')

        
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
    

    @property
    def is_updated(self) -> bool:
        return self.updated_at is not None


    def set_updated_by(self, user:KumbioUser):
        self.updated_by = user
        self.save()
    
    
    def get_calendars(self):
        return self.calendar_set.all()


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name} - {self.id}'



class MailTemplatesManager(models.Model):
    
    """
    
        !IMPORTANT NOTE: THIS MANAGER OBJECT MUST ONLY HAVE ONE RECORD IN THE DATABASE
    
    """
    
    next_template_to_start_at:int = models.IntegerField()
    
    def increase_next_template_to_start_at(self):
        """
            _summary_: The next_template_to_start_at must increase by the number of default templates 
            (currently 6) that are added to a user when they are created.
            
        """
        
        NUMBER_OF_TEMPLATES_TO_INCREASE = 7
        
        self.next_template_to_start_at += NUMBER_OF_TEMPLATES_TO_INCREASE
        self.save()
    
    
    def __str__(self) -> str:
        return f'Next starts at: {self.next_template_to_start_at}'