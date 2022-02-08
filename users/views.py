import json
import bcrypt
import jwt

from django.forms    import ValidationError
from django.http     import JsonResponse
from django.views    import View
from django.conf     import settings

from users.models    import User
from users.utils     import Validation, login_decorator

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
        
class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data          = json.loads(request.body)

            cart, created = Cart.objects.get_or_create(user_id = user.id, product_id = data["product_id"])
            
            if not created:
                cart.quantity = F('quantity') + 1
                cart.save()
                return JsonResponse({'message' : 'ADD_QUANTITY_IN_CART'}, status=200)
            
            return JsonResponse({'message' : 'ADD_CART'}, status = 201)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def get(self, request):
        user        = request.user.id
        carts       = Cart.objects.filter(user_id = user).select_related('product').prefech_related('images')
        total_price = carts.aggregate(total_price = Sum(F('product__price') * F('quantity')))
        
        result = [{
            'total_price' : total_price,
            'cart'        : [{
                'cart_id'        : cart.id,
                'korean_name'    : cart.product.korean_name,
                'english_name'   : cart.product.english_name,
                'price'          : cart.product.price,
                'quantity'       : cart.quantity,
                'image'          : [image.image_url for image in cart.product.images.all()][0],
                'sum_price'      : cart.product.price * cart.quantity,
            } for cart in carts]
        }]

        return JsonResponse({'carts' : result}, status = 200)
        
    # DELETE :8000/carts/1
    # DELETE :8000/carts?ids=[1, 2, 3]
    @login_decorator
    def delete(self, request, cart_id):
        try:
            Cart.objects.get(user_id = request.user.id, id=cart_id).delete()

            return JsonResponse({'message' : 'DELETE_CART'}, status = 200)

        except Cart.DoesNotExist as e:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_CART'}, status = 400)
        
    # PATCH :8000/carts/1
    @login_decorator
    def patch(self, request, cart_id): 
        try:
            data         = json.loads(request.body)
            user         = request.user
            quantity     = data['quantity']
            
            if int(quantity) < 1:
                return JsonResponse({'message' : 'DESELECTED_QUANTITY'}, status = 400)

            cart          = Cart.objects.get(user_id = user.id, id = cart_id)
            cart.quantity = quantity
            cart.save()    
                
            return JsonResponse({'message' : 'CHANGED_QUANTITY'}, status = 200)
        
        except Cart.DoesNotExist as e:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_CART'}, status = 400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)
