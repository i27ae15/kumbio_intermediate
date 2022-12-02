import secrets
import datetime

from django.db import models
from django.utils import timezone

from organization_info.models import Organization, OrganizationService, PaymentMethodAcceptedByOrg
from inventory.models import InventoryItem

import user_info.models as user_models


# Create your models here.

class InvoiceStatus(models.IntegerChoices):

    PAID = 1
    PENDING = 2
    CANCELLED = 3


class AppointmentInvoice(models.Model):

    appointment_id:int = models.IntegerField()

    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    payment_method:PaymentMethodAcceptedByOrg = models.ForeignKey(PaymentMethodAcceptedByOrg, on_delete=models.CASCADE)

    services = models.ManyToManyField(OrganizationService)
    
    amount:float = models.DecimalField(max_digits=10, decimal_places=2)
    status:int = models.IntegerField(choices=InvoiceStatus.choices)

    products:models.ManyToManyField = models.ManyToManyField(OrganizationService)
    
    payment_date:datetime.datetime = models.DateField(null=True, blank=True)
    payment_reference:str = models.CharField(max_length=50, null=True, blank=True)
    payment_note:str = models.CharField(max_length=50, null=True, blank=True)
    payment_remarks:str = models.CharField(max_length=50, null=True, blank=True)


    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='professional_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_deleted_by')
    
    # ----------------- Payment Methods ----------------- #

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.invoice_number
    

    class Meta:
        verbose_name = 'Appointment Invoice'
        verbose_name_plural = 'Appointment Invoices'
