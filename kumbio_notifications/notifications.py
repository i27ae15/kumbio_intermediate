import requests

from .validators import validate_email, validate_phone_number
from .enums import MessageChannel

KUMBIO_COMMUNICATIONS_ENDPOINT = 'https://communications-api.kumbio.com/'

def send_notification(token_for_app:str, organization_id:int, send_to:list[str], date_time_to_send:list[str]=['NOW'], 
                      templates:list[int]=None, messages:list[str]=None, subjects:list[str]=None, 
                      extra_data:dict=None, data_to_replace:dict=None):
    
    """

        the main keys are the templates and the messages, if not templates then messsage will be used and with messages the subjects also will be used,
        for each message there must be a subject, and a datetime to send
       
        for each send_to, there is going to be a message attach to that email or phone number

        for example:
        
            send_notification(
                send_to=['email1'],
                date_time_to_send=['2115-09-01 12:00:00', '2115-09-01 13:00:00'],
                templates=[1, 2]
            )
            
            these parameters will create two notifications, one with template 1 and the other with template 2, both will be sent to email1
            the first template will take the date_time_to_send[0] and the second template will take the date_time_to_send[1]
            
            --------------------------------------------------------------------------------------------------------------------------------
            
            send_notification(
                send_to=['email1', 'email2'],
                date_time_to_send=['2115-09-01 12:00:00', '2115-09-01 13:00:00'],
                templates=[1, 2]
            )
            
            these parameters will create four notifications, two with template 1 and the other two with template 2, they will be sent to email1 
            and email2, the first template will take the date_time_to_send[0] and the second template will take the date_time_to_send[1]
            
            --------------------------------------------------------------------------------------------------------------------------------

            so, basically
            
            total_number_of_notications = len(send_to) * len(templates|messages), 
            
            where:
                len(date_time_to_send) == len(templates)  = 1, or
            if instead of templates using messages and subjects and messages:
                len(messages) == len(subjects) == len(date_time_send)
                
            send_to_will be validated by check_if_email or check_if_phone_number,
            
            first checking if the email is valid, if not then check for phone number, if neither of them are valid, then raise an exception    
    """
    
    # making validations
    
    if templates is None and messages is None:
        raise Exception('templates or messages must be provided')
    
    if messages and subjects is None:
        raise Exception('subjects must be provided if messages are provided')
    
    if messages and len(messages) != len(subjects):
        raise Exception('the length of messages and subjects must be the same')
    
    if messages and len(messages) != len(date_time_to_send) or templates and len(date_time_to_send) != len(templates):
        raise Exception('the length of date_time_to_send must be the same as the length of templates or messages')
    
    
    messages_to_send:list = messages if messages else templates
    send_subjects:bool = True if messages else False
    send_template:bool = True if templates else False
    
    message_channel = MessageChannel.EMAIL
    for send in send_to:
        
        if not validate_email(send):
            if not validate_phone_number:
                raise Exception(f'{send} is not a valid email or phone number')
            message_channel = MessageChannel.SMS

        # once we've validated the email or phone number, we can send the notification
        
        data_to_send = {
            'organization_id': organization_id,
            'send_to': send,
        }
        
        if data_to_replace:
            data_to_send['data_to_replace'] = data_to_replace
        
        if message_channel == MessageChannel.EMAIL:
            data_to_send['send_to_email'] = send
        elif message_channel == MessageChannel.SMS:
            data_to_send['send_to_phone'] = send
        
        
        for index, message in enumerate(messages_to_send):
            
            data_to_send['date_time_to_send'] = date_time_to_send[index]
            
            if send_template:
                data_to_send['template'] = message # sending the id of the template
            else:
                data_to_send['message'] = message
            
            if send_subjects:
                data_to_send['subject'] = subjects[index]
            
            if extra_data is not None:
                data_to_send['extra_data'] = extra_data
            
            res = requests.post(
                url=f'{KUMBIO_COMMUNICATIONS_ENDPOINT}notifications/',
                headers={
                    'Authorization': f'Token {token_for_app}'
                },
                data=data_to_send
            )
            
            if res.status_code != 201:
                raise Exception(res.json())
    
    # TODO: Check the models and add the necessary fields to save the 