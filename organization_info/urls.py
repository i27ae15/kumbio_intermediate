from django.urls import path
from .views import OrganizationProfessionalAPI, OrganizationPlaceAPI, OrganizationView, OrganizationSectorView

app_name = 'organization_info'

urlpatterns = [
    path('organization/', OrganizationView.as_view(), name='organization'),
    path('professionals/', OrganizationProfessionalAPI.as_view(), name='professional'),
    path('places/', OrganizationPlaceAPI.as_view(), name='place'),
    path('sectors/', OrganizationSectorView.as_view(), name='sector'),
]