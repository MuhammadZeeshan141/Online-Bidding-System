from django.contrib import admin
from .models import Countries, Order, OrderMessage


# Register your models here.

class CountriesAdmin(admin.ModelAdmin):
    search_fields = ['sortName', 'name', 'phoneCode']


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['firstName', 'lastName', 'email', 'country', 'city', 'ZIP', 'product__title', 'phoneNumber',
                     'status']

    list_filter = ['date', 'status', 'ZIP', 'city', 'country']


class MessageAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return OrderMessage.objects.all()
        else:
            return OrderMessage.objects.filter(vendor=request.user)

    search_fields = ['customer', 'vendor', 'date']

    list_filter = ['customer', 'vendor', 'date']


admin.site.register(Countries, CountriesAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderMessage, MessageAdmin)
