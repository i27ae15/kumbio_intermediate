# python
import requests
import os

# django 
import secrets
from django.contrib.auth import get_user_model # If used custom user model
from django.db.models.query import QuerySet

# rest-framework
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Swagger
from drf_yasg.utils import swagger_auto_schema

# models 
from user_info.models import KumbioUser
from organization_info.models.main_models import Organization
from organization_info.models.email_template_models import MailTemplate, MailTemplatesManager

# serializers 
from organization_info.serializers import OrganizationSerializer
from user_info.serializers import UserCustomSerializer, CreateUserSerializer


# others
from utils.default_templates import DEFAULT_TEMPLATES

from dotenv import load_dotenv

load_dotenv()

CALENDAR_ENDPOINT = os.environ['CALENDAR_ENDPOINT']


# functions

def create_default_templates(organization:Organization) -> int:

    template_manager:MailTemplatesManager = MailTemplatesManager.objects.get(id=1)
    starts_at:int = template_manager.next_template_to_start_at

    for template in DEFAULT_TEMPLATES:
        template['organization'] = organization
        MailTemplate.objects.create(**template)

    template_manager.increase_next_template_to_start_at()
    
    return starts_at

    
@api_view(['GET'])
def check_if_invited(request, link):
    
    try: organization:Organization = Organization.objects.get(invitation_link=link)
    except: return Response({'invited_by': False})
    
    serializer = OrganizationSerializer(organization)
    
    return Response({'invited_by': serializer.data})


@swagger_auto_schema()
@api_view(['POST'])
def verify_user(request):
    
    """Verify user email

    body parameters:
    
        code (str): el codigo para verificar al usuario
    
    Returns:
        _type_: _description_
    """
    
    
    code = request.data['code']

    try: user:KumbioUser = KumbioUser.objects.get(code_to_verify_email=code)
    except KumbioUser.DoesNotExist: return Response({'error':'El codigo no es valido'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.verify_code()
    
    return Response({'message':'El usuario ha sido verificado'}, status=status.HTTP_200_OK)


@swagger_auto_schema()
@api_view(['POST'])
def send_email_verification(request):
    
    """ Send email verification
    
    body parameters:

        user_id (int): id del usuario al que se le va a enviar el correo de verificacion

    Returns:
        _type_: _description_
    """
    
    user_id = request.data['user_id']
    
    try: user:KumbioUser = KumbioUser.objects.get(id=user_id)
    except KumbioUser.DoesNotExist: return Response({'error':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
    user.send_verification_code()
    
    return Response({'message':'El codigo ha sido enviado'}, status=status.HTTP_200_OK)


@swagger_auto_schema()
@api_view(['GET'])
def check_if_email_and_username_exist(request):
    
    email = request.GET.get('email')
    username = request.GET.get('username')
    
    exist_email = False
    username_exist = False
    
    if email:
        exist_email = KumbioUser.objects.filter(email=email).exists()
    
    if username:
        username_exist = KumbioUser.objects.filter(username=username).exists()
    
    return Response({'email':exist_email, 'username':username_exist}, status=status.HTTP_200_OK)


class CustomObtainAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        
        """Iniciar sesion
        
        Se necesita el email, pero por alguna razon que no voy a ver ahorita, tienes que pasar el campo del email 
        con el nombre del username, es decir:
        
        username: ejemplode@email.com

        Returns:
            _type_: _description_
        """

        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token:Token = Token.objects.get(key=response.data['token'])
        token.user:KumbioUser = token.user
        
        
        if not token.user.is_email_verified:
            return Response({'error': 'Email no verificado', 'user_id': token.user.id}, status=status.HTTP_401_UNAUTHORIZED)
            

        organization:Organization = Organization.objects.get(id=token.user.organization.id)
        organization_serializer = OrganizationSerializer(organization)
        return Response(
            {
                'token': token.key, 
                'name': token.user.get_full_name(),
                'role': token.user.role,
                'id': token.user.id,
                'organization': organization_serializer.data,
            })
    

class CreateUserAPI(APIView):   
    @swagger_auto_schema()
    def post(self, request):
        
        """Crear a un nuevo usuario
        
        Para crear al usuario se debe pasar el id de la organizacion a la que pertenece; de no tener un id valido,
        el usuario debe crear la organzacion, pasando el nombre de la organizacion y el numer de telefono del usuario que la creara.
        
        
        body parameters:
            
            En caso de que el usuario tenga un id valido de organizacion:
                
                organization (int): id de la organizacion a la que pertenece el usuario
    
            ----------------------------------------------------------------------------        
            
            En caso de que el usuario no tenga un id valido de organizacion:
    
                organization (dict): {
                    name (str): nombre de la organizacion,
                    phone (str): telefono del usuario que creara la organizacion
                    email (str): email del usuario que creara la organizacion
                }
                phone (str): numero de telefono del usuario que creara la organizacion
                
            para ambos casos:
            
                firts_name (str): nombre del usuario
                last_name (str): apellido del usuario
                email (str): email del usuario
                username (str): username del usuario
                password (str): password del usuario

        Returns:
            _type_: _description_
        """
        
        
        organization_data = request.data['organization']
        organization_id:int = None
        
        try: organization_id = int(organization_data)
        # this will create the organization, assuming that the person that is being created is the owner of the organization
        except TypeError:            
            organization:Organization = Organization.objects.create(
                # org info
                name=organization_data['name'],
                email=organization_data['email'],
                phone=organization_data['phone'],
                
                # owner info
                owner_email=request.data['email'],
                owner_first_name=request.data['first_name'],
                owner_last_name=request.data['last_name'],
                owner_phone=request.data['phone'],
                )
            organization_id = organization.id          
        
        
        request.data['organization'] = organization_id
        
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            # creating the user in the calendar app so we can obtain the token for the user in calendar
            res = requests.post(f'{CALENDAR_ENDPOINT}register/api/v2/create-user/', json={
                'organization_id': organization_id,
                'email':request.data['email'],
                'first_name': organization_data['name'],
                'last_name': organization_data['name'],
                'role': 1,
            })
            
            organization.set_default_template_starts_at(create_default_templates(organization))
            
            user:KumbioUser = serializer.instance
            user.set_password(request.data['password'])
            user.calendar_token = res.json()['token']
            user.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        organization.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
