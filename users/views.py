import json
import bcrypt
import jwt

from django.forms    import ValidationError
from django.http     import JsonResponse
from django.views    import View
from django.conf     import settings

from users.models    import User
from users.utils     import Validation, login_decorator

signup_rules = [
    UserNamevalidationRule(max_length = 10, min_length = 5), 
    PasswordValidationRule(),
    BirthDateValidationRule(),
    PhoneNumberValidationRule()
]

signin_rules = [
    UserNamevalidationRule(max_length = 100, min_length = 500), 
    PasswordValidationRule(),
]

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
            validator       = UserValidation(signup_rules)
            validator.validate(user)
            
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
            validator       = UserValidation(signin_rules)
            validator.validate(user)
            
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
