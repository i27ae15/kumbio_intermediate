import datetime
from django.db import models
from django.utils import timezone

from user_info.models import KumbioUser
from .main_models import Organization

class CalendarSettings(models.Model):
    
    organization:Organization = models.ForeignKey(Organization, null=True, default=None, on_delete=models.CASCADE)
    
    send_notification_to:str = models.EmailField(null=True, default=None)
    send_first_notification:int = models.IntegerField(null=True, blank=True, default=24)
    send_second_notification:int = models.IntegerField(null=True, blank=True, default=None)
    send_third_notification:int = models.IntegerField(null=True, blank=True, default=None)
    
    template_to_send_as_confirmation = models.IntegerField(null=True, default=None)
    template_to_send_as_reminder_1 = models.IntegerField(null=True, default=None)
    template_to_send_as_reminder_2 = models.IntegerField(null=True, default=None)
    template_to_send_as_reminder_3 = models.IntegerField(null=True, default=None)
    template_to_send_as_rescheduled = models.IntegerField(null=True, default=None)
    template_to_send_as_canceled = models.IntegerField(null=True, default=None)
    template_to_send_as_new_client_to_calendar_user = models.IntegerField(null=True, default=None)
    template_to_send_as_rescheduled_to_calendar_user = models.IntegerField(null=True, default=None)
    template_to_send_as_canceled_to_calendar_user = models.IntegerField(null=True, default=None)
    
    # logs fields
    
    datetime_created:datetime.datetime = models.DateTimeField(default=timezone.now)
    datetime_updated:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)
    datetime_deleted:datetime.datetime = models.DateTimeField(default=None, null=True, blank=True)

    created_by:KumbioUser = models.ForeignKey(KumbioUser, on_delete=models.CASCADE, related_name='calendar_settings_created_by')
    updated_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='calendar_settings_updated_by')
    deleted_by:KumbioUser = models.ForeignKey(KumbioUser, null=True, on_delete=models.CASCADE, default=None, related_name='calendar_settings_deleted_by')