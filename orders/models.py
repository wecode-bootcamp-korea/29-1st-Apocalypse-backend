from django.db import models

class Cart(models.Model):
    quantity     = models.IntegerField()
    user         = models.ForeignKey("users.User",on_delete=models.CASCADE,related_name="carts")
    product      = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='carts')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carts'
        
class Wishlist(models.Model):
    user         = models.ForeignKey("users.User",on_delete=models.CASCADE,related_name='wishlists')
    product      = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='wishlists')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wishlists'
        
class OrderStatus(models.Model):
    status = models.CharField(max_length=50)
    created_at   = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'order_statuses'

class Order(models.Model):
    user         = models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='orders')
    status       = models.ForeignKey('OrderStatus',on_delete=models.CASCADE,related_name='orders')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        
class OrderItemStatus(models.Model):
    status       = models.CharField(max_length=50)
    created_at   = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'order_item_statuses'

class OrderItem(models.Model):
    product           = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='order_items')
    order             = models.ForeignKey('Order',on_delete=models.CASCADE,related_name='order_items')
    order_item_status = models.ForeignKey('OrderItemStatus',on_delete=models.CASCADE,related_name='order_items')
    quantity          = models.IntegerField()
    price             = models.DecimalField(max_digits=15,decimal_places=2)

    class Meta:
        db_table = 'order_items'