import json

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Q

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
                'subcategory_image': subcategory.image_url,
                'product_list' : [{
                    'id'   : product.id,
                    'name' : product.korean_name 
                        } for product in subcategory.products.all()]
                } for subcategory in category.sub_categories.all()]
            } for category in categories]

        return JsonResponse({'message':'SUCCESS' ,'Category' : result}, status=200)

class ProductList(View):
    def get(self,request):
        try:
            category_name    = request.GET.getlist('category', None)
            subcategory_name = request.GET.getlist('subcategory', None)
            sorting          = request.GET.get('sort', None)
            limited          = request.GET.get('limited', None)
            q =Q()
            
            if category_name:
                q &= Q(subcategory__category__name__in = category_name)
            
            if subcategory_name:
                q &= Q(subcategory__name__in = subcategory_name)
            
            if limited:
                q &= Q(english_name__icontains = "limited")

            
            products = Product.objects.filter(q)
            
            if sorting == "price":
                products = products.order_by("price")
            elif sorting == "-price":
                products = products.order_by("-price")
            elif sorting == "date":
                products = products.order_by("created_at")
            elif sorting == "-date":
                products = products.order_by("-created_at") 
                            
            result = [{
                "id"           : product.id,
                "korean_name"  : product.korean_name,
                "english_name" : product.english_name,
                "price"        : round(product.price),
                "image"        : [image.image_url for image in product.images.filter(product_id = product.id)][0],
                "description"  : product.description
            }for product in products]
        
            return JsonResponse({'message':'SUCCESS' ,'Product' : result}, status=200)
        
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
