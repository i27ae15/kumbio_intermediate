# python
import datetime
import pytz
import math

# pandas
import pandas as pd


from print_pp.logging import Print


def tz_diff(date, tz1:pytz.timezone, tz2:pytz.timezone):
    """
        Returns the difference in hours between timezone1 and timezone2
        for a given date.
    """
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


def get_start_and_end_time(exclusion_list:list[list[float]], convert_to_utc=False, timezone=None) -> tuple[str, str]:
    """_summary_

    Args:
        exclusion_list (list[list]): The list of excluded time that is going to be used
        will look something like this: [[0, 7], [10, 11], [18, 23]]

    Returns:
        _type_: _description_
    """
    
    if convert_to_utc:

        exclusion_list = change_exclusion_timezone(exclusion_list, timezone, 'UTC')
        return exclusion_list, convert_float_to_minutes(float(exclusion_list[0][-1])), convert_float_to_minutes(float(exclusion_list[-1][0]))
    else:
        return convert_float_to_minutes(float(exclusion_list[0][-1])), convert_float_to_minutes(float(exclusion_list[-1][0]))


def change_exclusion_timezone(exclusion_list:list[list[float]], from_timezone:str, to_timezone:str) -> list[list[float]]:

    """
        Converts a list of time intervals in one timezone to another timezone.

        Parameters:
        exclusion_list (list[list[float]]): A list of time intervals, where each interval is represented as a list of two floats between 0 and 23.99, representing the start and end times in the `from_timezone`.
        from_timezone (str): The timezone in which the input time intervals are represented, e.g. 'US/Eastern'.
        to_timezone (str): The timezone to which the time intervals should be converted, e.g. 'UTC'.

        Returns:
        list[list[float]]: A list of time intervals with the same format as `exclusion_list`, but with the start and end times converted to the `to_timezone`.

        Example:
        >>> exclusion_list = [[9, 11], [20, 22]]
        >>> change_exclusion_timezone(exclusion_list, 'US/Eastern', 'UTC')
        [[14, 16], [1, 3]]
    """

    
    diff = tz_diff(datetime.datetime.now().date(), pytz.timezone(from_timezone), pytz.timezone(to_timezone))
    for i in range(len(exclusion_list)):
        exclusion_list[i][0] += diff if exclusion_list[i][0] + diff < 24 else diff - 24
        exclusion_list[i][1] += diff if exclusion_list[i][1] + diff < 24 else diff - 24
        
    return exclusion_list
