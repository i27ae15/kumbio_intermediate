from django.urls import path
from .views import (OrganizationProfessionalView, OrganizationPlaceView, OrganizationView, 
OrganizationSectorView, OrganizationServiceView, OrganizationClientView, OrganizationClientDashboardInfoView,
OrganizationServiceDashboardInfoView, OrganizationProfessionalDashboardInfoView, OrganizationPlaceDashboardInfoView,
ClientForLandingPage, get_organization_client_types)

app_name = 'organization_info'

urlpatterns = [
    path('organization/', OrganizationView.as_view(), name='organization'),
    path('professionals/', OrganizationProfessionalView.as_view(), name='professional'),
    path('places/', OrganizationPlaceView.as_view(), name='place'),
    path('sectors/', OrganizationSectorView.as_view(), name='sector'),
    path('services/', OrganizationServiceView.as_view(), name='service'),
    path('clients/', OrganizationClientView.as_view(), name='client'),

    # functions
    path('client_types/', get_organization_client_types, name='client_types'),

    
    # For client dashboard
    path('organization-dashboard-info/', OrganizationClientDashboardInfoView.as_view(), name='organization_dashboard_info'),
    path('service-dashboard-info/', OrganizationServiceDashboardInfoView.as_view(), name='service_dashboard_info'),
    path('staff-dashboard-info/', OrganizationProfessionalDashboardInfoView.as_view(), name='staff_dashboard_info'),
    path('place-dashboard-info/', OrganizationPlaceDashboardInfoView.as_view(), name='place_dashboard_info'),
    
    # For Calendar
    path('client-for-calendar/', ClientForLandingPage.as_view(), name='client_for_landing_page'),


    # path('extra_fields_for_client_type/', get_extra_fields_for_client_type, name='extra_fields_for_client_type'),

]

