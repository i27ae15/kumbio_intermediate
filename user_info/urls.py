from django.urls import path
from .views import authenticate_user

urlpatterns = [
    path('authenticate-user/', authenticate_user)
]