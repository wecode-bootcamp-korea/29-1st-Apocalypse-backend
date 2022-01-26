from django.urls import path

from products.views import CategoryList, NewProductList, FeaturingProductList

urlpatterns = [
    path('/category', CategoryList.as_view()),
    path('/product', NewProductList.as_view()),
    path('/featuring', FeaturingProductList.as_view()),
]
