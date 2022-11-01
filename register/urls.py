from django.urls import path, re_path
from .views import check_if_invited, verify_user, send_email_verification, check_if_email_and_username_exist, CreateUserAPI, CustomObtainAuthToken


urlpatterns = [
    path('check-link/<str:link>', check_if_invited),
    path('verify-user/', verify_user),
    path('send-email-verification/', send_email_verification),
    path('check-if-user-exists/', check_if_email_and_username_exist),
    path('create-user/', CreateUserAPI.as_view()),
    re_path(r'^authenticate/', CustomObtainAuthToken.as_view()),
]