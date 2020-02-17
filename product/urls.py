from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("products", views.product_index, name="product_index"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("category/<int:pk>/", views.products_by_category, name="products_by_category"),
]