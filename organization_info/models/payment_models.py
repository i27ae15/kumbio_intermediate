# Python
import datetime

# Django
from django.db import models
from django.utils import timezone

# Models
from .main_models import (Organization, OrganizationClient, OrganizationProfessional, OrganizationService, 
                          OrganizationPromotion, OrganizationPlace)

from user_info.models import KumbioUser


class InvoiceStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PAID = 2, 'Paid'
    CANCELED = 3, 'Canceled'
    

class PaymentMethodAcceptedByOrg(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='payment_methods_accepted')
    payment_method:str = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.id} - {self.organization.name} - {self.payment_method}'


class Invoice(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client:OrganizationClient = models.ForeignKey(OrganizationClient, on_delete=models.CASCADE)
    service:OrganizationService = models.ForeignKey(OrganizationService, on_delete=models.CASCADE)
    professional:OrganizationProfessional = models.ForeignKey(OrganizationProfessional, on_delete=models.CASCADE)
    promotion:OrganizationPromotion = models.ForeignKey(OrganizationPromotion, on_delete=models.CASCADE, null=True, blank=True)
    place:OrganizationPlace = models.ForeignKey(OrganizationPlace, on_delete=models.CASCADE, null=True, blank=True, default=None)
    
    
    amount:float = models.FloatField()
    discount:int = models.IntegerField(default=None)
    total:float = models.FloatField()
    tax:float = models.FloatField()
    
    referral_code:str = models.CharField(max_length=255, null=True, blank=True)
    
    status:int = models.IntegerField(choices=InvoiceStatus.choices)
    
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetimne_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:KumbioUser = models.ForeignKey(KumbioUser, on_delete=models.CASCADE, related_name='invoice_created_by')
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='invoice_updated_by')
    deleted_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='invoice_deleted_by')

    
    def __str__(self):
        return f'{self.id} - {self.client.first_name} {self.client.last_name} - {self.organization.name}'
    
