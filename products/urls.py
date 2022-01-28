from django.urls import path

from products.views import (
    CategoryList,
    ProductList,
)

urlpatterns = [
    path('/categories', CategoryList.as_view()),
    path('', ProductList.as_view()),
]
