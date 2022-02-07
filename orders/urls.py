from django.urls import path

from orders.views import OrderCheckout, OrderCancel

urlpatterns = [
    path('', OrderCheckout.as_view()),
    path('/cancel', OrderCancel.as_view()),
]
