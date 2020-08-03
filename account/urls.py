from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("AccountDetails", views.accountDetails, name="accountDetails"),
    path("ContactVendor/<int:pk>/", views.contactVendor, name="contactVendor"),
    path("SendMessage/", views.sendMessage, name="sendMessage"),
]