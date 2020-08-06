from django.urls import path
from . import views

urlpatterns = [
    path("place-your-bid", views.placeYourBid, name="placeYourBid"),
    path("bidding", views.bidding_index, name="bidding_index"),
    path("coming_soon_bidding", views.coming_soon_bidding_index, name="coming_soon_bidding_index"),
    path("bidding/<int:pk>/<str:type>/", views.bidding_detail, name="bidding_detail"),
    path("bidding_category/<int:pk>/<str:type>/", views.bidding_by_category, name="bidding_by_category"),
    path("bidding-asc/<str:type>/", views.bidding_ascending, name="bidding_ascending"),
    path("bidding-desc/<str:type>/", views.bidding_descending, name="bidding_descending"),

]
