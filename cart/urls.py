from django.urls import path
from . import views

urlpatterns = [
    path("add-to-cart", views.addToCart, name='addToCart'),
    path("cart", views.cart, name='cart'),
    path("remove_cart_item", views.remove_cart_item, name='remove_cart_item'),
    path("checkout", views.checkout, name='checkout'),
    path("confirmation", views.confirmation, name='confirmation'),
    path("cart_item_increment", views.cart_item_increment, name='cart_item_increment'),
    path("cart_item_decrement", views.cart_item_decrement, name='cart_item_decrement'),
    path("orders", views.orders, name='orders'),
]
