from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    cart         = models.ManyToManyField("products.Product",through="Cart", related_name='user_cart_product')
    wishlist     = models.ManyToManyField("products.Product",through="Wishlist", related_name= 'user_wishlist_product')
    review       = models.ManyToManyField("products.Product",through="Review", related_name= 'user_review_product')
    
    class Meta:
        db_table = "users"

class Cart(models.Model):
    quantity     = models.IntegerField()
    user         = models.ForeignKey("User",on_delete=models.CASCADE,related_name="carts")
    product      = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='carts')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carts'
        
class Wishlist(models.Model):
    user         = models.ForeignKey("User",on_delete=models.CASCADE,related_name='wishlists')
    product      = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='wishlists')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wishlists'
                

class Review(models.Model):
    user         = models.ForeignKey('User',on_delete=models.CASCADE,related_name='reviews')
    product      = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='reviews')
    content      = models.CharField(max_length=600)
    rating       = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'        
        
        