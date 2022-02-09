import re
import jwt

from django.core.exceptions import ValidationError
from django.http  import JsonResponse
from django.conf  import settings
             
from users.models import User

class EmailValidation:
    def __init__(self, email, rules):
        self.email = email
        self.rules = rules
        
    def email_validator(email, rules):
        if not re.match(rules, email):
            raise ValidationError('INVALID_EMAIL')
        
class PasswordValidation:
    def __init__(self, password, rules):
        self.password = password
        self.rules    = rules
    
    def password_validator(password, rules):
        if not re.match(rules, password):
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
