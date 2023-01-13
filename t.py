import os
import requests
from threading import Thread

from .validators import validate_email, validate_phone_number
from .enums import MessageChannel, ObjectType

# external libraries
from dotenv import load_dotenv
load_dotenv()

from print_pp.logging import Print

KUMBIO_COMMUNICATIONS_ENDPOINT = os.getenv('KUMBIO_COMMUNICATIONS_ENDPOINT')
CURRENT_APP = os.getenv('CURRENT_APP') 

def start_new_thread(function):
    def decorator(*args, **kwargs):
        if kwargs.get('execute_in_another_thread'):
            t = Thread(target = function, args=args, kwargs=kwargs)
            t.daemon = True
            t.start()
        else:
            return function(*args, **kwargs)
            
    return decorator


@start_new_thread
def send_notification(token_for_app:str, organization_id:int, send_to:list[str], date_time_to_send:list[str]=['NOW'], 
                      templates:list[int]=None, messages:list[str]=None, subjects:list[str]=None, 
                      extra_data:dict=None, data_to_replace:dict=None, notification_type:object=None, treat_not_sent:bool=True,
                      execute_in_another_thread:bool=False, object_id:int=None, object_type:ObjectType=None, extra_object_data:dict=None):
    
    """
        the main keys are the templates and the messages, if not templates then message will be used and with messages the subjects also will be used,
        for each message there must be a subject, and a datetime to send
       
        for each send_to, there is going to be a message attach to that email or phone number

        for example:
            
            send_notification(
                send_to=['email1', 'email2'],
                date_time_to_send=['2115-09-01 12:00:00', '2115-09-01 13:00:00'],
                templates=[1, 2]
            )
            
            these parameters will create two notifications, one with template 1 that will be sent to the first send_to[0] 
            and the second with template 2 that will be sent to the second send_to[1]

            --------------------------------------------------------------------------------------------------------------------------------
            
            send_notification(
                send_to=['email1'],
                date_time_to_send=['2115-09-01 12:00:00', '2115-09-01 13:00:00'],
                templates=[1, 2]
            )
            
            these parameters will produce an error since they aren't the same length
            
            --------------------------------------------------------------------------------------------------------------------------------

            so, basically
            
            total_number_of_notications = len(send_to)
            
            where:
                len(date_time_to_send) == len(templates) == len(send_to), or
            if instead of templates using messages and subjects and messages:
                len(messages) == len(subjects) == len(date_time_send) == len(send_to)
                
            they have to be all the same length
            
        --------------------------------------------------------------------------------------------------------------------------------
                
        send_to_will be validated by check_if_email or check_if_phone_number,
        
        first checking if the email is valid, if not then check for phone number, if neither of them are valid, then raise an exception
        
        since a notification can be attached to a certain object such an appointment class, the object_id and the object_type must be passed
        to be able to identify this notification as a part of that object
        
        extra_object_data is a dictionary that can be used to pass extra data to the object, for example, if the object is an appointment, 
        the the extra data would look like this:
        
            appointment_id:int = being the id of the appointment

            calendar_id:int = being the id of the calendar that the appointment is attached to
            client_id:int = being the id of the client that the appointment is attached to
            
            professional_id:int = being the id of the professional that the appointment is attached to
            place_id:int = being the id of the place that the appointment is attached to
                
    """
    
    # making validations
    
    if templates is None and messages is None:
        raise Exception('templates or messages must be provided')
    
    if messages and subjects is None:
        raise Exception('subjects must be provided if messages are provided')
    
    if messages and len(messages) != len(subjects):
        raise Exception('the length of messages and subjects must be the same')
    
    if messages and len(messages) != len(date_time_to_send) or \
    templates and len(date_time_to_send) != len(templates) or len(date_time_to_send) != len(send_to):
        raise Exception('the length of date_time_to_send must be the same as the length of templates or messages')
    
    
    messages_to_send:list = messages if messages else templates
    send_subjects:bool = True if messages else False
    send_template:bool = True if templates else False
    
    message_channel = MessageChannel.EMAIL
    
    data_to_send = {
        'organization_id': organization_id,
        'object_id': object_id,
        'object_type': object_type.value if object_type else None,
        'extra_object_data': extra_object_data if extra_object_data else None,
    }
    
    for index, send in enumerate(send_to):
        
        if not validate_email(send):
            if not validate_phone_number:
                raise Exception(f'{send} is not a valid email or phone number')
            message_channel = MessageChannel.SMS

        # once we've validated the email or phone number, we can send the notification
        data_to_send['send_to'] = send
       
        if data_to_replace:
            data_to_send['data_to_replace'] = data_to_replace
        
        if message_channel == MessageChannel.EMAIL:
            data_to_send['send_to_email'] = send
        elif message_channel == MessageChannel.SMS:
            data_to_send['send_to_phone'] = send
        
        data_to_send['date_time_to_send'] = date_time_to_send[index]
        
        if send_template:
            data_to_send['template_id'] = messages_to_send[index] # sending the id of the template
        else:
            data_to_send['message'] = messages_to_send[index]
        
        if send_subjects:
            data_to_send['subject'] = subjects[index]
        
        if extra_data is not None:
            data_to_send['extra_data'] = extra_data
        
        status_code = None

        try:
            res = requests.post(
                url=f'{KUMBIO_COMMUNICATIONS_ENDPOINT}notifications/',
                headers={
                    'Authorization': token_for_app
                },
                json=data_to_send,
            )
            status_code = res.status_code
        except requests.ConnectionError:
            status_code = 500

            
        if status_code != 201 and CURRENT_APP == 'KUMBIO_CALENDAR' and treat_not_sent:
                from calendar_logs.utils import create_new_notification_log_entry
                
                data_for_serializer = data_to_send.copy()
                data_for_serializer['notification_type'] = notification_type
                data_for_serializer['error'] = 'Epale, papa, no se pudo enviar la notificación'
                data_for_serializer['notification_channel'] = message_channel.value
                
                data_for_serializer['error'] = res.json()
                create_new_notification_log_entry(data_for_serializer)
                
        else:
            return status_code == 201
        
           