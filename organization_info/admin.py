from django.contrib import admin
from .models import (
    Organization, FrequentlyAskedQuestion, OrganizationCampaigns, OrganizationClient, OrganizationPlace, 
    OrganizationProfessional, OrganizationPromotion, OrganizationService, ProfessionalSpecialty, 
    PaymentMethodAcceptedByOrg, Sector, OrganizationClientType, DayAvailableForPlace, DayAvailableForProfessional,
    ClientParent, OrganizationClientDocument
)


admin.site.register(Organization)
admin.site.register(FrequentlyAskedQuestion)
admin.site.register(OrganizationCampaigns)
admin.site.register(OrganizationClient)
admin.site.register(OrganizationPlace)
admin.site.register(OrganizationProfessional)
admin.site.register(OrganizationPromotion)
admin.site.register(OrganizationService)
admin.site.register(Sector)
admin.site.register(ProfessionalSpecialty)
admin.site.register(PaymentMethodAcceptedByOrg)
admin.site.register(OrganizationClientType)
admin.site.register(DayAvailableForPlace)
admin.site.register(DayAvailableForProfessional)
admin.site.register(ClientParent)
admin.site.register(OrganizationClientDocument)
