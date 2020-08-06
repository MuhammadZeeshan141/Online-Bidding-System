from django.db import models


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    long_description = models.TextField(null=True)
    image = models.ImageField(upload_to='pics')
    price = models.IntegerField()
    available = models.BooleanField()
    quantity = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()
    category = models.ForeignKey('Category', related_name="products", on_delete=models.CASCADE)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateTimeField(
        auto_now_add=True,
    )
    PURCHASE = 'purchase'
    BID = 'bid'
    BOTH = 'both'
    TYPE = [
        (PURCHASE, 'Product is for purchase'),
        (BID, 'Product is for bid'),
        (BOTH, 'Product is for both'),
    ]
    type = models.CharField(max_length=35, choices=TYPE, default=PURCHASE)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)
    status = models.BooleanField()

    def __str__(self):
        return self.title


class History(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date = models.DateTimeField(
        auto_now_add=True,
    )
