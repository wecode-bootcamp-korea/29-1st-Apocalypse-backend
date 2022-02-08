import re
import jwt

from django.core.exceptions import ValidationError
from django.http  import JsonResponse
from django.conf  import settings
             
from users.models import User

class Validation():
    def __init__(self, email, password):
        self.email     = email
        self.password  = password
        
    def email_validator(email):
        REGEX_EMAIL    = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(REGEX_EMAIL, email):
            raise ValidationError('INVALID_EMAIL')
    def login_validator_email
        REGEX_EMAIL2    = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
    def password_validator(password):
        REGEX_PASSWORD = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        if not re.match(REGEX_PASSWORD, password):
            raise ValidationError('INVALID_PASSWORD')
        
def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)         
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)  
            request.user = User.objects.get(id=payload['user_id'])

        except jwt.exceptions.DecodeError:                                  
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=401)

        except User.DoesNotExist:                                        
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper



class UserValidationRule:
    def validate(self, user):
        return all(getattr(self, 'validate_' + key)(user) for key in self.__dict__.keys())

class UserNamevalidationRule(UserValidationRule):
    def __init__(self, max_length, min_length):
        self.max_length = max_length
        self.min_length = min_length

    def validate_min_length(self, user):
        return len(user["name"]) > self.min_length
    
    def validate_max_length(self, user):
        return len(user["name"]) < self.max_length
   
class PhoneNumberValidationRule(UserValidationRule):
    def __init__(self):
        self.phone_number_regex = ""

    def validate_phone_number_regex(self, user):
        return re.match(self.phone_number_regex, user.phone_number 
 
class UserValidation:
    def __init__(self, rules):
        self.rules = rules

    def validate(self, user):
        return all(rule.validate(user) for rule in self.rules)


# signup views.py
user  = {"name" : "홍홍홍", "phone_number" : "010-7402-0990"}
rules = [
    UserNamevalidationRule(max_length = 10, min_length = 5), 
    PasswordValidationRule(),
    BirthDateValidationRule(),
    PhoneNumberValidationRule()
]

validation = UserValidationRule(rules)
validation.validate(user)

# signin views.py
user  = {"name" : "홍홍홍", "password" : "xxxxxxx"}
rules = [
    UserNamevalidationRule(max_length = 10, min_length = 5), 
    PasswordValidationRule(),
]

validation = UserValidationRule(rules)
validation.validate(user)lass UserValidationRule:
    def validate(self, user):
        return all(getattr(self, 'validate_' + key)(user) for key in self.__dict__.keys())

class UserNamevalidationRule(UserValidationRule):
    def __init__(self, max_length, min_length):
        self.max_length = max_length
        self.min_length = min_length

    def validate_min_length(self, user):
        return len(user["name"]) > self.min_length
    
    def validate_max_length(self, user):
        return len(user["name"]) < self.max_length
   
class PhoneNumberValidationRule(UserValidationRule):
    def __init__(self):
        self.phone_number_regex = ""

    def validate_phone_number_regex(self, user):
        return re.match(self.phone_number_regex, user.phone_number 
 
class UserValidation:
    def __init__(self, rules):
        self.rules = rules

    def validate(self, user):
        return all(rule.validate(user) for rule in self.rules)


# signup views.py
user  = {"name" : "홍홍홍", "phone_number" : "010-7402-0990"}
rules = [
    UserNamevalidationRule(max_length = 10, min_length = 5), 
    PasswordValidationRule(),
    BirthDateValidationRule(),
    PhoneNumberValidationRule()
]

validation = UserValidation(rules)
validation.validate(user)

# signin views.py
user  = {"name" : "홍홍홍", "password" : "xxxxxxx"}
rules = [
    UserNamevalidationRule(max_length = 100, min_length = 500), 
    PasswordValidationRule(),
]

validation = UserValidation(rules)
validation.validate(user)
