from django.contrib import admin
from .models import KumbioToken, ClientDashboardToken

admin.site.register(KumbioToken)
admin.site.register(ClientDashboardToken)
