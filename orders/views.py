import json

from django.views         import View
from django.http          import JsonResponse
from django.db            import transaction
from django.db.models     import Sum, F
from django.db.utils      import IntegrityError

from orders.models        import (
        Order, 
        OrderItem, 
        PaymentMethod, 
        OrderStatusEnum, 
        OrderItemStatusEnum
)
from users.models         import Cart
from users.utils          import login_decorator

class OrderView(View):
    @login_decorator
    def post(self,request):
        try:
            with transaction.atomic():
                data           = json.loads(request.body)
                user           = request.user
                carts          = Cart.objects.filter(user_id = user.id).select_related("user","product")
                payment_method = data.get('payment')
                
                order = Order.objects.create(
                    user            = user,
                    status          = OrderStatusEnum.CONFIRMING.value,
                    payment_method  = PaymentMethod.objects.get(name = payment_method)
                )
                
                OrderItem.objects.bulk_create([OrderItem(
                        product  = cart.product,
                        order    = order,
                        status   = OrderItemStatusEnum.PAID.value,
                        quantity = cart.quantity,
                        price    = cart.product.price,
                    )for cart in carts])
                
                carts.delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'INVALID_PAYMENT_METHOD'}, status=400)
        
    @login_decorator
    def get(self,request):
        user   = request.user
        orders = Order.objects.filter(user=user).select_related('user').prefetch_related('order_items')
        total_price = orders.aggregate(total_price = Sum(F('order_items__price') * F('order_items__quantity')))
        
        result = [{
            'order_id'    : order.id,
            'user'        : order.user.id,
            'user_name'   : order.user.name,
            'total_price' : total_price,
            'order_item_list' :[{
                'id'           : orderitem.product.id,
                'korean_name'  : orderitem.product.korean_name,
                'english_name' : orderitem.product.english_name,
                'status'       : orderitem.status.status,
                'quantity'     : orderitem.quantity, 
                'price'        : orderitem.product.price,
                'sum_price'    : orderitem.price * orderitem.quantity
            }for orderitem in order.order_items.all()]
        } for order in orders]
            
        return JsonResponse({'message': 'SUCCESS', 'result' : result}, status=200)

    @login_decorator
    def patch(self, request ,order_id):
        try:
            with transaction.atomic():         
                order    = Order.objects.prefetch_related("order_items").get(user_id = request.user.id, id = order_id)   
                
                order.status = OrderStatusEnum.ORDER_CANCELLED.value
                order.save()
                
                order.order_items.all().update(status = OrderItemStatusEnum.ORDER_CANCELLED.value)
                
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except IntegrityError:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_ORDER'}, status = 400)
