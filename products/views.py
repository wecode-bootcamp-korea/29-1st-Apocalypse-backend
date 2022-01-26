import json

from django.views         import View
from django.http          import JsonResponse

from products.models import *

class CategoryList(View):
    def get(self,request):
        categories = Category.objects.all()

        result = [{
            'id'            : category.id,
            'category_name' : category.name,
            'subcategory_list' :[{
                'id'   : subcategory.id,
                'name' : subcategory.name,
                'product_list' : [{
                    'id'   : product.id,
                    'name' : product.korean_name 
                        } for product in subcategory.products.all()]
                } for subcategory in category.sub_categories.all()]
            } for category in categories]

        return JsonResponse({'message':'SUCCESS' ,'result' : result}, status=200)
    
class FeaturingProductList(View):
    def get(self,request):
        feature_products = Product.objects.filter(english_name__contains = 'Limited')
        
        result = [{
            'id'            : product.id,
            'korean_name'   : product.korean_name,
            'image'         : [image.image_url for image in product.images.filter(product_id = product.id)][0] 
        } for product in feature_products]
        
        return JsonResponse({'message':'SUCCESS' ,'result' : result}, status=200)

class NewProductList(View):
    def get(self,request):
        new_products = Product.objects.filter(id__lte=5).order_by('created_at')
        
        result = [{
            'id'            : product.id,
            'korean_name'   : product.korean_name,
            'english_name'  : product.english_name,
            'price'         : product.price,
            'image'         : [image.image_url for image in product.images.filter(product_id = product.id)][0]
        } for product in new_products]
        
        return JsonResponse({'message':'SUCCESS' ,'신제품 리스트' : result}, status=200)
    

