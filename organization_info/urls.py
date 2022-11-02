from django.urls import path
from .views import OrganizationProfessionalAPI, OrganizationPlaceAPI

app_name = 'organization_info'

urlpatterns = [
    path('professionals/', OrganizationProfessionalAPI.as_view(), name='professional'),
    path('places/', OrganizationPlaceAPI.as_view(), name='place'),
]