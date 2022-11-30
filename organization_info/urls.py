from django.urls import path
from .views import (OrganizationProfessionalAPI, OrganizationPlaceAPI, OrganizationView, 
OrganizationSectorView, OrganizationServiceView, OrganizationClientView, get_organization_client_types, get_extra_fields_for_client_type)

app_name = 'organization_info'

urlpatterns = [
    path('organization/', OrganizationView.as_view(), name='organization'),
    path('professionals/', OrganizationProfessionalAPI.as_view(), name='professional'),
    path('places/', OrganizationPlaceAPI.as_view(), name='place'),
    path('sectors/', OrganizationSectorView.as_view(), name='sector'),
    path('services/', OrganizationServiceView.as_view(), name='service'),
    path('clients/', OrganizationClientView.as_view(), name='client'),

    # functions
    path('client_types/', get_organization_client_types, name='client_types'),
    # path('extra_fields_for_client_type/', get_extra_fields_for_client_type, name='extra_fields_for_client_type'),

]