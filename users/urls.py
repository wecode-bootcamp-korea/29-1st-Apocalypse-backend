from django.urls import path

from users.views import SignUpView, SignInView, CartView
urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/cart',   CartView.as_view()),
    path('/cart/<int:cart_id>',   CartView.as_view()),
]