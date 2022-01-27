from django.urls import path

from products.views import CategoryList

urlpatterns = [
    path('/categories', CategoryList.as_view()),
]
