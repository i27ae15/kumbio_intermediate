from .email_template_models import (MailTemplate, MailTemplatesManager)
from .main_models import (Organization, OrganizationClient, OrganizationProfessional, OrganizationService, OrganizationCampaings,
                        OrganizationPlace, OrganizationPromotion, OrganizationProduct, FrequentlyAskedQuestion, 
                        ProfessionalSpeciality, Rating, Sector)
from .payment_models import (Invoice, PaymentMethodAcceptedByOrg)
from .app_setting_models import (CalendarSettings)



# class Plan(models.Model):
#     description:str = models.TextField()
        
#     max_number_of_users:int = models.IntegerField(default=1)
#     max_number_of_calendars:int = models.IntegerField(default=2)
#     max_number_of_appoinments:int = models.IntegerField(default=150)

#     name:str = models.CharField(max_length=100)
    
#     price:float = models.DecimalField(max_digits=6, decimal_places=2)

#     def __str__(self):
#         return self.name

