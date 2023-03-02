from threading import Thread

from rest_framework.response import Response
from rest_framework import status, exceptions
from organization_info.models.main_models import Organization, OrganizationService


from user_info.info import ADMIN_ROLE_ID


def start_new_thread(function):
    def decorator(*args, **kwargs):
        if kwargs.get('execute_in_another_thread'):
            t = Thread(target = function, args=args, kwargs=kwargs)
            t.daemon = True
            t.start()
        else:
            return function(*args, **kwargs)
    return decorator


def check_if_user_is_admin_decorator(func, *args, **kwargs):
    def wrapper(self, request, *args, **kwargs):
        if request.user.role.id == ADMIN_ROLE_ID:
            return func(self, request, *args, **kwargs)
        else:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


def check_if_user_is_admin(request, raise_exceptions=True) -> bool:
    if request.user.role.id == ADMIN_ROLE_ID:
        return True
    else:
        if raise_exceptions:
            raise exceptions.PermissionDenied(_("You are not authorized to perform this action"))
        else:
            return False


@start_new_thread
def delete_services_from_professionals_availability(organization:Organization, service:OrganizationService, execute_in_another_thread:bool=True):
    for professional in organization.professionals:
        for day in professional.available_days:
            day.delete_service(service_id=service.pk)