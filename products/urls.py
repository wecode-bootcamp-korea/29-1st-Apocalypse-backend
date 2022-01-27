from django.urls import path

from products.views import (
    CategoryList,
    MainPageProductList,
)

urlpatterns = [
    path('/categories', CategoryList.as_view()),
    path('/main', MainPageProductList.as_view()),
]
