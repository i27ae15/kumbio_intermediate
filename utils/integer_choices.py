from django.db import models

class RatingMadeBy(models.IntegerChoices):
    CLIENT = 1, 'Client'
    PROFESSIONAL = 2, 'Professional'
    
    