from django.urls import path
from .views import authenticate_user, get_available_places_for_user, get_available_services_for_user,  get_kumbio_user, NotificationsSettingsView

app_name = 'user_info'

urlpatterns = [
    path('notifications-settings/', NotificationsSettingsView.as_view()),

    path('authenticate-user/', authenticate_user),
    path('get-kumbio-user/', get_kumbio_user),
    path('get-available-services-for-user/', get_available_services_for_user, name='get_available_services_for_user'),
    path('get-available-places-for-user/', get_available_places_for_user, name='get_available_places_for_user'),
]