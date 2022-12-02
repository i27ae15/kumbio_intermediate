import datetime

from django.db import models
from django.utils import timezone

import user_info.models as user_models

# Create your models here.

class InventoryItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)
    deleted_at:datetime.datetime = models.DateTimeField(default=None, blank=True, null=True)

    created_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, on_delete=models.CASCADE, related_name='professional_created_by')
    updated_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_updated_by')
    deleted_by:user_models.KumbioUser = models.ForeignKey(user_models.KumbioUser, blank=True, null=True, on_delete=models.CASCADE, default=None, related_name='professional_deleted_by')
    

    def __str__(self):
        return self.name