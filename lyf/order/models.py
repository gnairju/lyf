from django.db import models
from cart.models import cart
from user.models import CustomUser,userAddress
from adminPanel.models import Product,coupons
from datetime import datetime

class order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address = models.ForeignKey(userAddress,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    days_needed=models.PositiveIntegerField(default=3)
    date = models.DateField(default=datetime.now)
    del_date=models.DateField(default=datetime.now)
    ret_date = models.DateField(default=datetime.now)
    total_price = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    caution_deposit = models.PositiveBigIntegerField()
    delivery_charge = models.PositiveBigIntegerField(default=40)
    platform_charges = models.PositiveBigIntegerField(default=10)
    total_charges = models.PositiveBigIntegerField(default=0)
    coupon = models.OneToOneField(coupons, related_name='order', null=True, blank=True, on_delete=models.SET_NULL)

    STATUS_CHOICES = [
        ('confirmed','confirmed'),
        ('Taken', 'Taken'),
        ('Shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('rental_period','rental_period'),
        ('returned','returned'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )


