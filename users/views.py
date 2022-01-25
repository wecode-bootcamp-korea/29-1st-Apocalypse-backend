import json
import re
import bcrypt
import jwt

from django.http    import JsonResponse
from django.views   import View
from django.conf    import settings

from users.models   import User

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
            
            if not re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message' : 'INVALID EMAIL'},       status = 400)
            if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', password):
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