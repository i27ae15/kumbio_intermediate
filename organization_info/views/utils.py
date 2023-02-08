from rest_framework.response import Response
from rest_framework import status, exceptions


from user_info.info import ADMIN_ROLE_ID



def check_if_user_is_admin_decorator(func, *args, **kwargs):
    def wrapper(self, request, *args, **kwargs):
        if request.user.role.id == ADMIN_ROLE_ID:
            return func(self, request, *args, **kwargs)
        else:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


def check_if_user_is_admin(request) -> 'True | Response':
    if request.user.role.id == ADMIN_ROLE_ID:
        return True
    else:
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
