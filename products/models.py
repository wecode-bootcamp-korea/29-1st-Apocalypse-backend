from django.db import models

class Category(models.Model):
    name         = models.CharField(max_length=50)
    created_at   = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "categories"
        
class Subcategory(models.Model):
    name         = models.CharField(max_length=50)
    category     = models.ForeignKey("Category",on_delete=models.CASCADE, related_name='sub_categories')
    created_at   = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subcategories'
    
class Product(models.Model):
    korean_name  = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    price        = models.DecimalField(max_digits=15,decimal_places=2)
    description  = models.TextField()
    how_to_use   = models.TextField()
    subcategory  = models.ForeignKey("Subcategory",on_delete=models.CASCADE, related_name="products")
    components   = models.ManyToManyField("Component", through="ProductComponent")
    preferences  = models.ManyToManyField("Preference", through="ProductPreference")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'

class Image(models.Model):
    image_url    = models.URLField()
    product      = models.ForeignKey("Product",on_delete=models.CASCADE,related_name='images')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'images'

class Component(models.Model):
    name         = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        db_table = 'components'

class Preference(models.Model):
    name         = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'preferences'

class ProductComponent(models.Model):
    product      = models.ForeignKey("Product",on_delete=models.CASCADE, related_name="productcomponent_products")
    component    = models.ForeignKey("Component",on_delete=models.CASCADE, related_name="productcomponent_components")

    class Meta:
        db_table = 'products_components'
        
class ProductPreference(models.Model):
    product      = models.ForeignKey("Product",on_delete=models.CASCADE, related_name='productpreference_products')
    preference   = models.ForeignKey("Preference",on_delete=models.CASCADE, related_name='productpreference_preferencess')
    
    class Meta:
        db_table = 'products_preferences'