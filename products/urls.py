from django.urls import path

from products.views import (
    CategoryList,
    ProductList,
    ProductDetailView
)

urlpatterns = [
    path('/categories', CategoryList.as_view()),
    path('', ProductList.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view())
]
