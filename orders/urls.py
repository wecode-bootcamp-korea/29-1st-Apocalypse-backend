from django.urls import path

from orders.views import OrderCheckout

urlpatterns = [
    path('', OrderCheckout.as_view()),
]
