import jwt, json

from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM             
from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)         
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)  
            request.user = User.objects.get(id=payload['user_id'])
            
        except jwt.exceptions.DecodeError:                                  
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=401)

        except User.DoesNotExist:                                        
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
        
        return func(self, request, *args, **kwargs)

    return wrapper
