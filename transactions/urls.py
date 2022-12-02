from django.urls import path
from .views import AppointmentInvoiceViewSet

app_name = 'transactions'

urlpatterns = [
    path('appointment-invoice/', AppointmentInvoiceViewSet.as_view(), name='appointment_invoice'),
]