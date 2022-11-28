# python
import datetime
import pytz
import math
import pandas as pd
from dateutil import tz

def convert_utc_time_to_local_time(timezone:str, utc_time:str) -> str:
    """_summary_

    This will convert the utc time to local time
       
    Returns:
        tuple: (response dict) (status of the response)
    """
    
    current_year = datetime.datetime.now().year
    utc_time = f'{current_year} {utc_time}'

    # convert time_to_check to a datetime.datetime object
    utc_time = datetime.datetime.strptime(utc_time, '%Y %H:%M:%S')

    # convert the time to local time
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(timezone)
    
    utc = utc_time.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)

    return central.strftime('%H:%M:%S')
        
        
def convert_local_time_to_utc(timezone:str, local_time:str, get_only_time=False, return_in_string=True) -> 'str | datetime.datetime':
    
    """_summary_

    This will convert the local time to utc time
       
    Returns:
        tuple: (response dict) (status of the response)
    """

    # convert time_to_check to a datetime.datetime object
    if get_only_time:
        local_time:datetime.datetime = datetime.datetime.strptime(local_time, '%H:%M:%S')
    else:
        local_time:datetime.datetime = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')

    # convert the time to local time
    from_zone = tz.gettz(timezone)
    to_zone = tz.gettz('UTC')
    
    local = local_time.replace(tzinfo=from_zone)
    utc = local.astimezone(to_zone)

    minutes = str()
    if local_time.minute < 10:
        minutes = f'0{local_time.minute}'

    if get_only_time:
        if return_in_string:
            return f'{utc.strftime("%H")}:{minutes}:00'
        else:
            return datetime.time(int(utc.strftime('%H')), int(local_time.strftime('%M')), int(utc.strftime('%S')))

    if return_in_string:
        return f'{utc.strftime("%Y-%m-%d %H")}:{minutes}:00'
    else:
        return datetime.datetime(int(utc.strftime('%Y')), int(utc.strftime('%m')), int(utc.strftime('%d')), int(utc.strftime('%H')), int(local_time.strftime('%M')), int(utc.strftime('%S')))

    

def tz_diff(date, tz1:pytz.timezone, tz2:pytz.timezone):
    '''
    Returns the difference in hours between timezone1 and timezone2
    for a given date.
    '''
    date = pd.to_datetime(date)
    return (tz1.localize(date) - tz2.localize(date).astimezone(tz1)).seconds / 3600
        
        
def convert_float_to_minutes(float_time:float) -> str:
    """_summary_

    Args:
        float_time (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    time = str()
    
    # taking the decimal and the integer part so that we can convert it to minutes
    decimal_part, integer_part = math.modf(float_time)

    # if it is less than 10, then it is a single digit number, so we add a 0 in front of it
    if float_time < 10:
        time = '0' + str(int(integer_part))
    else:
        time = str(int(integer_part))
    
    end_at_minute = decimal_part * 60
    
    if end_at_minute < 10:
        end_at_minute = '0' + str(int(end_at_minute))
    
    
    return f'{time}:{end_at_minute}:00'


def get_start_and_end_time(exclusion_list:list['list[float]'], convert_to_utc=False, timezone=None) -> tuple[str, str]:
        """_summary_

        Args:
            exclusion_list (list[list]): The list of excluded time that is going to be used
            will look something like this: [[0, 7], [10, 11], [18, 23]]

        Returns:
            _type_: _description_
        """
        
        if convert_to_utc:
            
            diff = tz_diff(datetime.datetime.now().date(), pytz.timezone(timezone), pytz.timezone('UTC'))
            for i in range(len(exclusion_list)):
                exclusion_list[i][0] += diff if exclusion_list[i][0] + diff < 24 else diff - 24
                exclusion_list[i][1] += diff if exclusion_list[i][1] + diff < 24 else diff - 24
                 
            return exclusion_list, convert_float_to_minutes(float(exclusion_list[0][-1])), convert_float_to_minutes(float(exclusion_list[-1][0]))
        else:
            return convert_float_to_minutes(float(exclusion_list[0][-1])), convert_float_to_minutes(float(exclusion_list[-1][0]))
        

# Is this function deprecated?
def check_time_interval(start_time:datetime.datetime, end_time:datetime.datetime) -> float:
    
    difference = start_time - end_time
    
    seconds_in_day = 24 * 60 * 60
    
    diff_in_minutes = divmod(difference.days * seconds_in_day + difference.seconds, 60)[0]
    
    interval = diff_in_minutes / 60
    
    return interval
