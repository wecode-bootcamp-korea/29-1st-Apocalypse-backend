import json
import bcrypt
import jwt

from django.forms    import ValidationError
from django.http     import JsonResponse
from django.views    import View
from django.conf     import settings

from users.models    import User
from users.validator import Validation

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
            
            Validation.email_validator(email)
            Validation.password_validator(password)
            
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
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)    
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            user_data       = json.loads(request.body)
            email           = user_data['email']
            password        = user_data['password']
            user            = User.objects.get(email = email)
            
            Validation.email_validator(email)
            Validation.password_validator(password)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
            
            access_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({'message' : 'SUCCESS', 'JWT' : access_token}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'DOES NOT EXIST USER'}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 400)