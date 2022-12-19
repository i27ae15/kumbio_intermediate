from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from rest_framework import exceptions

from organization_info.models.main_models import Organization, OrganizationPlace

from print_pp.logging import Print

def get_places(organization:Organization, place_id:int=None, return_as_query_set=False) -> 'QuerySet[OrganizationPlace] | OrganizationPlace':

    """

        La función get_places recibe tres parámetros:

        Parameters:
        - organization (Organization): Organización de la cual se quiere obtener el lugar.
        - place_id (int, optional): ID del lugar que se desea obtener. Si no se especifica, se obtienen todos los lugares de la organización.
        - return_as_query_set (bool, optional): Si es True, se devuelve un QuerySet de lugares en lugar de una instancia de OrganizationPlace. Por defecto es False.

        Returns:
        - QuerySet[OrganizationPlace] | OrganizationPlace: Lugar o conjunto de lugares de la organización especificada.

        La función retorna un QuerySet de OrganizationPlace si place_id es None o si return_as_query_set
        es True. Si place_id es un entero, retorna una instancia de OrganizationPlace. 
        Si no encuentra un lugar con el place_id especificado o si no hay lugares en la organización,
        lanza una excepción NotFound.
    
    """

    if not isinstance(organization, Organization):
        try:
            organization = Organization.objects.get(id=organization)
        except Organization.DoesNotExist:
            Print('exit at first except')
            raise TypeError(_(f'organization must be an instance of Organization not {type(organization)}'))


    if return_as_query_set or place_id is None:
        if place_id:
            places = OrganizationPlace.objects.filter(organization=organization.id, id=place_id)
        else:
            places = OrganizationPlace.objects.filter(organization=organization.id)
        
        
        if not places:
            Print('exit at second except')
            raise exceptions.NotFound(_('Place(s) not found'))
        
        Print('exit with success')
        return places

    try:
        return OrganizationPlace.objects.get(organization=organization.id, id=place_id)
    except OrganizationPlace.DoesNotExist:
        Print('exit at third except')
        raise exceptions.NotFound(_('Place not found'))