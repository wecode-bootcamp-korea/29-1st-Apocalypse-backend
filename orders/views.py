import json

from django.views         import View
from django.http          import JsonResponse
from json.decoder         import JSONDecodeError

from products.models      import Product
from orders.models        import Order, OrderItem, OrderStatus, OrderItemStatus, PaymentMethod
from users.models         import User, Cart
from users.utils          import login_decorator

class OrderCheckout(View):
    @login_decorator
    def post(self,request):
        try:
            data           = json.loads(request.body)
            user           = request.user
            carts          = Cart.objects.filter(user=user)
            contact        = data.get('contact')
            payment_method = request.GET.get('payment')
            
            order = Order.objects.create(
                user            = user,
                status          = OrderStatus.objects.get(status='입금확인중'),
                phone_number    = user.phone_number,
                address         = user.address,
                contact         = contact,
                payment_method  = PaymentMethod.objects.get(name=payment_method)
            )
            
            for cart in carts:
                OrderItem.objects.create(
                    product  = cart.product.id,
                    order    = order,
                    status   = OrderItemStatus.objects.get(status='상품준비중'),
                    quantity = cart.quantity,
                    price    = cart.product.price,
                )
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)
                
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
