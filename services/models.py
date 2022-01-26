from django.db import models

class Shop(models.Model):
    name         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    reservation  = models.ManyToManyField("users.User",through="Reservation", related_name='user_reservation_shop')
    created_at   = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        db_table = 'shops'
    

class Reservation(models.Model):
    time         = models.DateField()
    user         = models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='reservations')
    shop         = models.ForeignKey('Shop',on_delete=models.CASCADE,related_name='reservations')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reservations'