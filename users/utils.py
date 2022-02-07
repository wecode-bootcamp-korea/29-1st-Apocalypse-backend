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
