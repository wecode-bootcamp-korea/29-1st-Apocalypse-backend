from ast import Pass
import json
import bcrypt
import jwt

from django.db.utils import IntegrityError
from django.forms    import ValidationError
from django.http     import JsonResponse
from django.views    import View
from django.conf     import settings
from django.db.models import Sum, F

from users.models    import User, Cart, Wishlist
from users.utils     import PasswordValidation, EmailValidation, login_decorator

email_rules = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
password_rules = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

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
            
            EmailValidation.email_validator(email, email_rules)
            PasswordValidation.password_validator(password, password_rules)
            
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
            
            EmailValidation.email_validator(email, email_rules)
            PasswordValidation.password_validator(password, password_rules)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
            
            access_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
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

            cart, created = Cart.objects.get_or_create(user_id = request.user.id, product_id = data["product_id"])

            if not created:
                cart.quantity = F('quantity') + 1
                cart.save()
                return JsonResponse({'message' : 'ADD_QUANTITY_IN_CART'}, status=200)

            return JsonResponse({'message' : 'ADD_CART'}, status = 201)

        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except IntegrityError:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_IN_CART'}, status = 400)

    @login_decorator
    def get(self, request):
        user        = request.user.id
        carts       = Cart.objects.filter(user_id = user).select_related('product').prefetch_related('product__images')
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

    @login_decorator
    def delete(self, request, cart_id):
        try:
            Cart.objects.get(user_id = request.user.id, id=cart_id).delete()

            return JsonResponse({'message' : 'NO_CONTENT'}, status = 204)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_CART'}, status = 400)

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

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_CART'}, status = 400)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)

class WishlistView(View):
    @login_decorator
    def post(self, request):
        try:
            data          = json.loads(request.body)

            wishlist, created = Wishlist.objects.get_or_create(user_id = request.user.id, product_id = data["product_id"])

            if not created:
                wishlist.delete()
                
                return JsonResponse({'message' : 'NO_CONTENT'}, status=204)

            return JsonResponse({'message' : 'ADD_PRODUCT_IN_WISHLIST'}, status = 201)

        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except IntegrityError:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_IN_CART'}, status = 400)

    @login_decorator
    def get(self, request):
        user        = request.user.id
        wishlists = Wishlist.objects.filter(user_id=user).select_related("product")
        
        result = [{
            'wishlist' : wishlist.id,
            'korean_name'    : wishlist.product.korean_name,
            'english_name'   : wishlist.product.english_name,
            'price'          : wishlist.product.price,
            'image'          : [image.image_url for image in wishlist.product.images.all()][0],
        }for wishlist in wishlists]

        return JsonResponse({'wishlists' : result}, status = 200)

    @login_decorator
    def delete(self, request, wishlist_id):
        try:
            Wishlist.objects.get(user_id = request.user.id, id = wishlist_id).delete()

            return JsonResponse({'message' : 'NO_CONTENT'}, status = 204)

        except Wishlist.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_WISHLIST'}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDECODE_ERROR'}, status = 400)
