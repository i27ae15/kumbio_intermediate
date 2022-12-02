from django.contrib import admin
from .models import (Organization, FrequentlyAskedQuestion, OrganizationCampaigns, OrganizationClient, OrganizationPlace, 
                    OrganizationProduct, OrganizationProfessional, OrganizationPromotion, OrganizationService, ProfessionalSpecialty, 
                    PaymentMethodAcceptedByOrg, Sector, OrganizationClientType)


admin.site.register(Organization)
admin.site.register(FrequentlyAskedQuestion)
admin.site.register(OrganizationCampaigns)
admin.site.register(OrganizationClient)
admin.site.register(OrganizationPlace)
admin.site.register(OrganizationProduct)
admin.site.register(OrganizationProfessional)
admin.site.register(OrganizationPromotion)
admin.site.register(OrganizationService)
admin.site.register(Sector)
admin.site.register(ProfessionalSpecialty)
admin.site.register(PaymentMethodAcceptedByOrg)
admin.site.register(OrganizationClientType)