import json
import re
import bcrypt
import jwt

from django.http    import JsonResponse
from django.views   import View
from django.conf    import settings

from users.models   import User

REGEX_EMAIL    = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

class SignUpView(View):
    def post(self, request):
        try:
            user_data       = json.loads(request.body)
            name            = user_data['name']
            email           = user_data['email']
            address         = user_data['address']
            password        = user_data['password']
            phone_number    = user_data['phone_number']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message' : 'INVALID EMAIL'},       status = 400)
            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'message' : 'INVALID PASSWORD'},    status = 400)
            if User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'ALREADY EXIST EMAIL'}, status = 400)
            
            User.objects.create(  
                    email          = email,
                    password       = hashed_password,
                    name           = name,
                    phone_number   = phone_number,
                    address        = address,
                )
            return JsonResponse({'message' : 'CREATED'},  status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            user_data = json.loads(request.body)
            email           = user_data['email']
            password        = user_data['password']
            user            = User.objects.get(email = email)
            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message' : 'INVALID EMAIL'},     status = 400)
            elif not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'message' : 'INVALID PASSWORD1'}, status = 400)
            elif not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_PASSWORD2'}, status = 401)
            
            access_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({'message' : 'SUCCESS', 'JWT' : access_token}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'DOES NOT EXIST USER'}, status = 400)