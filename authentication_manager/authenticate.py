# python
import requests
import os
from dotenv import load_dotenv

# rest framework
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

# models
from django.utils.translation import gettext_lazy as _
from .models import KumbioToken

# others
from print_pp.logging import Print

load_dotenv()


class KumbioAuthentication(BaseAuthentication):
    
    keyword = 'Token'
    
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
    
    
    def authenticate_credentials(self, token):

        # get the token from the database
        try:
            token:KumbioToken = KumbioToken.objects.get(token=token)
        except KumbioToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return (token, token)

           
    def authenticate_header(self, request):
        return self.keyword