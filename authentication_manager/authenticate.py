# python
import requests
import os
from dotenv import load_dotenv

# rest framework
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

# models
from django.utils.translation import gettext_lazy as _
from .models import KumbioToken, ClientDashboardToken

# others
from print_pp.logging import Print

load_dotenv()


class KumbioAuthentication(BaseAuthentication):
    
    keyword = 'Token'
    main_model = None

    def get_model(self):
        if self.main_model is not None:
            return self.main_model
        from rest_framework.authtoken.models import Token
        return Token
    

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

        default_token = self.get_model()
        kumbio_token:KumbioToken = None
        def_token = None
        # get the token from the database
        try:
            kumbio_token:KumbioToken = KumbioToken.objects.get(token=token)
        except KumbioToken.DoesNotExist:
            try:
                def_token = default_token.objects.select_related('user').get(key=token)
            except default_token.DoesNotExist:
                raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if kumbio_token:
            return (kumbio_token, kumbio_token)

        return (def_token.user, def_token)

           
    def authenticate_header(self, request):
        return self.keyword


class ClientDashboardAuthentication(BaseAuthentication):

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

        verified_token:ClientDashboardToken = None
        # get the token from the database
        try:
            verified_token:ClientDashboardToken = ClientDashboardToken.objects.get(token=token)
        except ClientDashboardToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))


        class User:
            def __init__(self):
                self.is_authenticated = True

        return (User(), verified_token)

           
    def authenticate_header(self, request):
        return self.keyword