import json

from django.views         import View
from django.http          import JsonResponse

from products.models      import *

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

        return JsonResponse({'message':'SUCCESS' ,'Category' : result}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)
            result  = [
                {
                    'id'           : product.id,
                    'korean_name'  : product.korean_name,
                    'english_name' : product.english_name,
                    'price'        : product.price,
                    'description'  : product.description,
                    'how_to_use'   : product.how_to_use,
                    'images'       : [{'image_url' : image.image_url} for image in product.images.all()]
                }
            ]
            return JsonResponse({"product" : result}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'DOES NOT EXIST PRODUCT'}, status = 404)