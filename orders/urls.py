from django.urls import path

from orders.views import Order

urlpatterns = [
    path('', Order.as_view()),
    path('/<int:order_id>',Order.as_view()),
]
