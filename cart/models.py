from django.db import models
from product.models import Product
from django.contrib.auth.models import User


# Create your models here.
class Cart(models.Model):
    price = models.IntegerField()
    status = models.BooleanField()
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateTimeField(
        auto_now_add=True,
    )


class Countries(models.Model):
    sortName = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    phoneCode = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, default=" default@gmail.com")
    country = models.CharField(max_length=100)
    adressLine1 = models.CharField(max_length=100)
    adressLine2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    ZIP = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    productPrice = models.IntegerField()
    orderPrice = models.IntegerField()
    date = models.DateTimeField(
        auto_now_add=True,
    )
    PENDING = 'pending'
    CANCELED = 'canceled'
    DELIVERED = 'delivered'
    STATUS = [
        (PENDING, 'Order is Pending'),
        (CANCELED, 'Order is Canceled'),
        (DELIVERED, 'Order is Delivered'),
    ]
    status = models.CharField(max_length=32, choices=STATUS, default=PENDING)

    def __str__(self):
        return self.product.title


class OrderMessage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor')
    message = models.TextField()
    CUSTOMER = 'customer'
    VENDOR = 'vendor'
    STATUS = [
        (CUSTOMER, 'customer'),
        (VENDOR, 'vendor'),
    ]
    msg_from = models.CharField(max_length=32, choices=STATUS, default=CUSTOMER)
    date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.message
