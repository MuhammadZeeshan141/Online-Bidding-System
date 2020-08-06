from django.contrib import admin
from .models import Records, Transactions
from product.models import Product


# Register your models here.
class RecordsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(created_by=request.user, type='bid') | Product.objects.filter(
                created_by=request.user, type='both')
        return super(RecordsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Records.objects.all()
        else:
            return Records.objects.filter(product__created_by=request.user)


admin.site.register(Records, RecordsAdmin)
admin.site.register(Transactions)
