from django.urls import path
from .views import OrganizationProfessionalAPI

urlpatterns = [
    path('professionals/', OrganizationProfessionalAPI.as_view(), name='professional'),
]