from django.urls import path

from users.views import SignUpView, SignInView, CartView, WishlistView
urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/cart',   CartView.as_view()),
    path('/cart/<int:cart_id>',   CartView.as_view()),
    path('/wishlist', WishlistView.as_view()),
    path('/wishlist/<int:wishlist_id>', WishlistView.as_view()),
]
