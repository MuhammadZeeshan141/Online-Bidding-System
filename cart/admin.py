from django.contrib import admin
from .models import Countries, Order


# Register your models here.

class CountriesAdmin(admin.ModelAdmin):
    search_fields = ['sortName', 'name', 'phoneCode']


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['firstName', 'lastName', 'email', 'country', 'city', 'ZIP', 'product__title', 'phoneNumber', 'status']

    list_filter = ['date', 'status', 'ZIP', 'city', 'country']


admin.site.register(Countries, CountriesAdmin)
admin.site.register(Order, OrderAdmin)
