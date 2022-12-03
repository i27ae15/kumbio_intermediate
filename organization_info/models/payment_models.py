# Python

# Django
from django.db import models
 

class PaymentMethodAcceptedByOrg(models.Model):
    payment_method:str = models.CharField(max_length=100)
    is_active:bool = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.pk} - {self.payment_method}'


