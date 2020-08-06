from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("products", views.product_index, name="product_index"),
    path("products-asc", views.product_ascending, name="product_ascending"),
    path("products-desc", views.product_descending, name="product_descending"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("category/<int:pk>/", views.products_by_category, name="products_by_category"),
    path("recommendations/", views.recommendations, name="recommendations"),
    path("recommendations/bidding_products", views.bidding_recommendations, name="bidding_recommendations"),
    path("search", views.search, name="search"),
]