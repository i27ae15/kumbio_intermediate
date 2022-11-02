from django.contrib import admin
from .models import (Organization, Invoice, FrequentlyAskedQuestion, OrganizationCampaings, OrganizationClient, OrganizationPlace, 
                    OrganizationProduct, OrganizationProfessional, OrganizationPromotion, OrganizationService, ProfessionalSpeciality, 
                    PaymentMethodAcceptedByOrg, Sector, MailTemplate, MailTemplatesManager)


admin.site.register(Organization)
admin.site.register(Invoice)
admin.site.register(FrequentlyAskedQuestion)
admin.site.register(OrganizationCampaings)
admin.site.register(OrganizationClient)
admin.site.register(OrganizationPlace)
admin.site.register(OrganizationProduct)
admin.site.register(OrganizationProfessional)
admin.site.register(OrganizationPromotion)
admin.site.register(OrganizationService)
admin.site.register(Sector)
admin.site.register(ProfessionalSpeciality)
admin.site.register(PaymentMethodAcceptedByOrg)
admin.site.register(MailTemplate)
admin.site.register(MailTemplatesManager)