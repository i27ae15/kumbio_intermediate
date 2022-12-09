import secrets
import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions

from organization_info.models import (Organization, OrganizationService, PaymentMethodAcceptedByOrg, 
OrganizationClient, OrganizationProfessional, OrganizationPromotion, OrganizationPlace)
from inventory.models import InventoryItem

import user_info.models as user_models

from print_pp.logging import Print


# Create your models here.

class InvoiceStatus(models.IntegerChoices):

    PAID = 1
    PENDING = 2
    CANCELLED = 3


class AppointmentInvoice(models.Model):

    appointment_id:int = models.IntegerField()

    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='appointment_invoice_organization')
    payment_method:PaymentMethodAcceptedByOrg = models.ForeignKey(PaymentMethodAcceptedByOrg, on_delete=models.CASCADE, related_name='appointment_invoice_payment_method')
    client:OrganizationClient = models.ForeignKey(OrganizationClient, on_delete=models.CASCADE, related_name='appointment_invoice_client')
    professional:OrganizationProfessional = models.ForeignKey(OrganizationProfessional, on_delete=models.CASCADE, related_name='appointment_invoice_professional')
    place:OrganizationPlace = models.ForeignKey(OrganizationPlace, on_delete=models.CASCADE, related_name='appointment_invoice_place')
    promotion:OrganizationPromotion = models.ForeignKey(OrganizationPromotion, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='appointment_invoice_promotion')
    

    services = models.ManyToManyField(OrganizationService, related_name='appointment_invoice_services')
    products:models.ManyToManyField = models.ManyToManyField(OrganizationService, related_name='appointment_invoice_products', blank=True)
    
    amount:float = models.DecimalField(max_digits=10, decimal_places=2)
    status:int = models.IntegerField(choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)

    tax:float = models.DecimalField(max_digits=10, decimal_places=2)
    discount:float = models.DecimalField(max_digits=10, decimal_places=2)

    total:float = models.DecimalField(max_digits=10, decimal_places=2) # validate this
    # this total is the total after taxes and the discount
    total_paid:float = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    payment_date:datetime.date = models.DateField(null=True, blank=True)
    payment_reference:str = models.CharField(max_length=50, null=True, blank=True)
    payment_note:str = models.CharField(max_length=50, null=True, blank=True)

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='appointment_invoice_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='appointment_invoice_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='appointment_invoice_deleted_by')
    
    
    # ----------------- Properties ----------------- #

    @property
    def is_paid(self) -> bool:
        return self.status == InvoiceStatus.PAID.value
    

    @property
    def in_debt(self) -> bool:
        return self.total_paid < self.total
    

    @property
    def debt_amount(self) -> float:
        return float(self.total - self.total_paid)


    # ----------------- Methods ----------------- #

    def save(self, *args, **kwargs):

        total = round(float(self.amount + (self.amount * self.tax) - (self.amount * self.discount)), 2)

        if total != float(self.total):
            raise exceptions.ValidationError(_(f'The total is not correct, please check the amount, tax and discount. With the given data the total should be: {total}'))

        if self.total_paid == self.total:
            self.status = InvoiceStatus.PAID
            self.payment_date = timezone.now().date()

        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f'{self.pk} - {self.organization.name} - {self.amount}'
    

    class Meta:
        verbose_name = 'Appointment Invoice'
        verbose_name_plural = 'Appointment Invoices'
