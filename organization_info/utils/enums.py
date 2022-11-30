from django.db import models
from enum import Enum

"""

    This file will store the enumerators for the organization_info app.

    models.IntegerChoices inherits from Enum, so we can put them here

"""


class FieldType(Enum):
    TEXT = 'TEXT'
    NUMBER = 'NUMBER'


class DayName(models.IntegerChoices):
    MONDAY = 0, 'Monday'
    TUESDAY = 1, 'Tuesday'
    WEDNESDAY = 2, 'Wednesday'
    THURSDAY = 3, 'Thursday'
    FRIDAY = 4, 'Friday'
    SATURDAY = 5, 'Saturday'
    SUNDAY = 6, 'Sunday'


class OrganizationClientCreatedBy(models.IntegerChoices):
    CALENDAR = 1
    ORDERS = 2
    KUMBIO = 3
    COMMUNICATIONS = 4
    
