from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from organization_info.models.main_models import (
    OrganizationProfessional, OrganizationClient, OrganizationService,
)


@receiver(post_save, sender=OrganizationProfessional)
def increment_number_of_professionals(sender, instance:OrganizationProfessional, created, **kwargs):
    if created:
        instance.organization.increment_number_of_professionals()


@receiver(post_delete, sender=OrganizationProfessional)
def decrement_number_of_professionals(sender, instance:OrganizationProfessional, **kwargs):
    instance.organization.decrement_number_of_professionals()


# Signal-Handler für OrganizationClient-Modell
@receiver(post_save, sender=OrganizationClient)
def increment_number_of_clients(sender, instance:OrganizationClient, created, **kwargs):
    if created:
        instance.client_parent.organization.increment_number_of_clients()


@receiver(post_delete, sender=OrganizationClient)
def decrement_number_of_clients(sender, instance:OrganizationClient, **kwargs):
    instance.client_parent.organization.decrement_number_of_clients()


# Signal-Handler für OrganizationService-Modell
@receiver(post_save, sender=OrganizationService)
def increment_number_of_services(sender, instance:OrganizationService, created, **kwargs):
    if created:
        instance.organization.increment_number_of_services()


@receiver(post_delete, sender=OrganizationService)
def decrement_number_of_services(sender, instance:OrganizationService, **kwargs):
    instance.organization.decrement_number_of_services()