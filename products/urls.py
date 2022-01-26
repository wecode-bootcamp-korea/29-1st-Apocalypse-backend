from django.urls import path

from products.views import CategoryList, NewProductList, LimitedProductList

urlpatterns = [
    path('/category', CategoryList.as_view()),
    path('/new-product', NewProductList.as_view()),
    path('/limited-product', LimitedProductList.as_view()),
]
