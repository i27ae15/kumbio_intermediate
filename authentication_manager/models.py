import datetime
import secrets


from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from rest_framework import exceptions

from organization_info.models.main_models import Organization



# Create your models here.

class AppToken(models.IntegerChoices):
    CALENDAR = 1, 'Calendar'
    ORDERS = 2, 'Orders'
    KUMBIO = 3, 'Kumbio'
    COMMUNICATIONS = 4, 'Communications'


class KumbioToken(models.Model):

    # fields --------------------------------------------

    app:str = models.IntegerField(choices=AppToken.choices)
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, default=None)
    token:str = models.CharField(max_length=120, unique=True, editable=False)

    is_tester:bool = models.BooleanField(default=False)
    is_authenticated:bool = models.BooleanField(default=True, editable=False)

    # logs fields
    # these tokens only can be created with a user with access to the django console
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)
    deleted_at:datetime.datetime = models.DateTimeField(null=True, blank=True, default=None)

    def __repr__(self):
        return self.token
    

    def __str__(self):
        return self.token

    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.app == AppToken.COMMUNICATIONS:
                self.token = f'Communications-{secrets.token_hex(21)}'
            elif self.app == AppToken.CALENDAR:
                self.token = f'Calendar-{secrets.token_hex(21)}'
            elif self.app == AppToken.ORDERS:
                self.token = f'Orders-{secrets.token_hex(21)}'
            elif self.app == AppToken.KUMBIO:
                self.token = f'Kumbio-{secrets.token_hex(21)}'
                
        return super().save(*args, **kwargs)


class ClientDashboardToken(models.Model):
    
    token:str = models.CharField(max_length=120, unique=True, editable=False)
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now, editable=False)
    
    
    def __repr__(self):
        return self.token
    
    
    def __str__(self):
        return self.token


    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = secrets.token_hex(21)
        else:
            raise  exceptions.ValidationError(_('This token can not be updated'))

        return super().save(*args, **kwargs)


