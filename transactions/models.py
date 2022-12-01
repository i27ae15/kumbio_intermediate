import secrets
import datetime

from django.db import models
from django.utils import timezone

from organization_info.models import Organization
import user_info.models as user_models


# Create your models here.


class AppointmentInvoice(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    number = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_reference = models.CharField(max_length=50, null=True, blank=True)
    payment_note = models.CharField(max_length=50, null=True, blank=True)
    payment_status = models.CharField(max_length=50, null=True, blank=True)
    payment_remarks = models.CharField(max_length=50, null=True, blank=True)


    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='professional_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_deleted_by')
    


    def save(self, *args, **kwargs):


        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.invoice_number

    

    class Meta:
        verbose_name = 'Appointment Invoice'
        verbose_name_plural = 'Appointment Invoices'
