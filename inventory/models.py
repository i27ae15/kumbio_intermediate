import datetime

from django.db import models
from django.utils import timezone
from organization_info.models import Organization

import user_info.models as user_models

# Create your models here.


class InventoryItem(models.Model):
    organization:Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    photo = models.ImageField(upload_to=f'{organization.name}/products/photos/', null=True, blank=True)

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='inventory_item_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='inventory_item_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='inventory_item_deleted_by')
    

    def __str__(self):
        return self.name


class OrganizationProduct(models.Model):
    
    item:InventoryItem = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    
    name:str = models.CharField(max_length=255)
    sales_description:str = models.TextField()
    sales_price:int = models.IntegerField()
    
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='product_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='product_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='product_deleted_by')


    @property
    def is_available(self):
        return self.item.quantity > 0

    
    @property
    def profit_margin(self):
        return self.sales_price - self.item.unit_price


    def __str__(self):
        return f'{self.id} - {self.name} - {self.organization.name}'

