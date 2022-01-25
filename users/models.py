from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    carts        = models.ManyToManyField("products.Product",through="orders.Cart", related_name='carts')
    wishlists    = models.ManyToManyField("products.Product",through="orders.Wishlist", related_name= 'wishlists')
    reviews      = models.ManyToManyField("products.Product",through="services.Review", related_name= 'reviews')
    
    class Meta:
        db_table = "users"