from django.db import models
from product.models import Product,Category


# Create your models here.

class Records(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    minimumBid = models.IntegerField()
    maximumBid = models.IntegerField()

    def __str__(self):
        return self.product.title


class Transactions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    record = models.ForeignKey(Records, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    biddingAmount = models.IntegerField()
    phoneNumber = models.CharField(max_length=30, default=None)
    country = models.CharField(max_length=100, default=None)
    adressLine1 = models.CharField(max_length=100, default=None)
    adressLine2 = models.CharField(max_length=100, default=None)
    city = models.CharField(max_length=100, default=None)
    ZIP = models.CharField(max_length=50, default=None)
    PENDING = 'pending'
    REJECTED = 'rejected'
    APPROVED = 'approved'
    STATUS = [
        (PENDING, 'Order is Pending'),
        (REJECTED, 'Order is Rejected'),
        (APPROVED, 'Order is Approved'),
    ]
    status = models.CharField(max_length=32, choices=STATUS, default=PENDING)

    def __str__(self):
        return self.user.username


class BidHistory(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    record = models.ForeignKey(Records, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(
        auto_now_add=True,
    )
