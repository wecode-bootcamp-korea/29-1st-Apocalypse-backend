import json

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Sum
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
            carts          = Cart.objects.filter(user=user).select_related("user","product")
            contact        = data.get('contact', None)
            payment_method = data.get('payment')
            
            order = Order.objects.create(
                user            = user,
                status          = OrderStatus.objects.get(status='입금확인중').id,
                phone_number    = carts.user.phone_number,
                address         = carts.user.address,
                contact         = contact,
                payment_method  = PaymentMethod.objects.get(name = payment_method)
            )
            
            for cart in carts:
                OrderItem.objects.create(
                    product  = cart.product.id,
                    order    = order,
                    status   = OrderItemStatus.objects.get(status='상품준비중').id,
                    quantity = cart.quantity,
                    price    = cart.product.price,
                )
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)
                
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
    
    @login_decorator
    def get(self,request):
        try:
            user   = request.user
            orders = Order.objects.filter(user=user).select_related('user','product').prefetch_related('orderitem')
            
            result = [{
                'order_id'    : order.id,
                'user'        : order.user.id,
                'user_name'   : order.user.name,
                'total_price' : order.orderitems.aggregate(Sum('price')),
                'order_item_list' :[{
                    'id'      : orderitem.product.id,
                    'name'    : orderitem.product.name,
                    'status'  : orderitem.status,
                    'quantity': orderitem.quantity, 
                    'price'   : orderitem.product.price
                }for orderitem in orders.order_items.all()]
            } for order in orders]
            
            return JsonResponse({'message': 'SUCCESS', 'result' :f'{user.id},{result}'}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

class OrderCancel(View):
    @login_decorator
    def post(self,request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            order_id = data.get('order_id', None)            
            order    = Order.objects.filter(user = user, id = order_id).prefetch_related("orderitem")
            
            order.update(OrderStatus.objects.get(status='취소됨').id)
            
            for orderitem in order.orderitems.all():
                orderitem.update(OrderItemStatus.objects.get(status='취소됨').id)
            
            return JsonResponse({'message': 'SUCCESS', 'order_id' : order.id}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
