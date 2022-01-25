from django.db import models

class User(models.Model):
    name           = models.CharField(max_length=50)
    email          = models.EmailField(max_length=50, unique=True)
    address        = models.CharField(max_length=100)
    password       = models.CharField(max_length=200)
    phone_number   = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'users'