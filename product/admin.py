from django.contrib import admin
from .models import Product, Category


# Register your models here.
class ProductAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()
        else:
            return Product.objects.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    search_fields = ['title']

    exclude = ('created_by',)

    list_filter = ['category', 'created_by']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']

    list_filter = ['title']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
