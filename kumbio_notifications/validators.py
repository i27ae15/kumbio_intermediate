import phonenumbers
import re

def validate_email(email:str) -> bool:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def validate_phone_number(value):
    """ Return False if the value does not looks like a mobile telephone number.
    """
    regex1 = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    regex2=re.compile(r'[a-zA-Z]')
    try:
        if "-" in value:
            value=value.replace('-','')
        print(value)
        #print(value.isdigit())

        if (regex1.search(value) == None) and (regex2.search(value) == None):
            my_number = phonenumbers.parse(value)
            rule1 = phonenumbers.is_possible_number(my_number)#re.compile(r"(^[+0-9]{1,3})*([0-9]{10,11}$)")#(r'^(?:\+?44)?[07]\d{9,13}$')
            rule2=phonenumbers.is_valid_number(my_number)
           # rule3=carrier._is_mobile(number_type(phonenumbers.parse(value)))
            if rule1 == True and rule2 == True:
                print(rule1,rule2)
                return True
            else:
                return False
        else:
            return False
    except:
        return False