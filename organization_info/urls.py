from django.urls import path
from .views.auth_required.kumbio_auth import (
    OrganizationProfessionalView, OrganizationPlaceView, OrganizationView, OrganizationSectorView, 
    OrganizationServiceView, OrganizationClientView, OrganizationClientDocument, get_organization_client_types, 
    delete_available_day_for_professional, get_dashboard_information
)
from .views.auth_required.dash_auth import (
    OrganizationDashboardInfoView, OrganizationServiceDashboardInfoView, 
    OrganizationProfessionalDashboardInfoView, OrganizationPlaceDashboardInfoView,
)
from .views.auth_required.calendar_auth import (
    ClientForCalendar, get_client_for_calendar, increment_number_of_appointments, get_service_name
)

app_name = 'organization_info'

urlpatterns = [
    path('organization/', OrganizationView.as_view(), name='organization'),
    path('professionals/', OrganizationProfessionalView.as_view(), name='professional'),
    path('places/', OrganizationPlaceView.as_view(), name='place'),
    path('sectors/', OrganizationSectorView.as_view(), name='sector'),
    path('services/', OrganizationServiceView.as_view(), name='service'),
    path('clients/', OrganizationClientView.as_view(), name='client'),
    path('client/documents/', OrganizationClientDocument.as_view(), name='client_document'),
    path('principal-dashboard-info/', get_dashboard_information, name='dashboard_info'),
    
    path('professionals/day/', delete_available_day_for_professional, name='delete_available_day_for_professional'),

    # functions
    path('client_types/', get_organization_client_types, name='client_types'),

    
    # For client dashboard
    path('organization-dashboard-info/', OrganizationDashboardInfoView.as_view(), name='organization_dashboard_info'),
    path('service-dashboard-info/', OrganizationServiceDashboardInfoView.as_view(), name='service_dashboard_info'),
    path('staff-dashboard-info/', OrganizationProfessionalDashboardInfoView.as_view(), name='staff_dashboard_info'),
    path('place-dashboard-info/', OrganizationPlaceDashboardInfoView.as_view(), name='place_dashboard_info'),
    
    
    # For Calendar
    path('client-for-calendar/', ClientForCalendar.as_view(), name='client_for_calendar'),
    path('get-client-for-calendar/', get_client_for_calendar, name='get_client_for_calendar'),
    path('calendar/increment-number-of-appointments/', increment_number_of_appointments),
    path('calendar/get-service-name/', get_service_name),


    # path('extra_fields_for_client_type/', get_extra_fields_for_client_type, name='extra_fields_for_client_type'),
]

