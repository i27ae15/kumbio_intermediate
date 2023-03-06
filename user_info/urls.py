from django.urls import path
from .views import (authenticate_user, get_available_places_for_user,
get_available_services_for_user,  get_kumbio_user, recover_password, 
verify_recovery_password_code, change_password, NotificationsSettingsView,
ToDoListTaskView, ToDoListView)

app_name = 'user_info'

urlpatterns = [
    path('notifications-settings/', NotificationsSettingsView.as_view()),
    path('authenticate-user/', authenticate_user),
    path('get-kumbio-user/', get_kumbio_user),
    path('get-available-services-for-user/', get_available_services_for_user, name='get_available_services_for_user'),
    path('get-available-places-for-user/', get_available_places_for_user, name='get_available_places_for_user'),
    path('recover-password/', recover_password, name='recover_password'),
    path('verify-recovery-password-code/', verify_recovery_password_code, name='verify_recovery_password_code'),
    path('change-password/', change_password, name='change_password'),
    path('todo-list/', ToDoListView.as_view()),
    path('todo-list-task/', ToDoListTaskView.as_view())

]