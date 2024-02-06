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
    from_date = models.DateField()
    to_date = models.DateField()
    total_price = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    payment_provider = models.BooleanField(default=False)
    caution_deposit = models.PositiveBigIntegerField()
    delivery_charge = models.PositiveBigIntegerField(default=40)
    platform_charges = models.PositiveBigIntegerField(default=10)
    total_charges = models.PositiveBigIntegerField(default=0)
    coupon = models.OneToOneField(coupons, related_name='order', null=True, blank=True, on_delete=models.SET_NULL)
    offer_total_price= models.PositiveBigIntegerField(default=0)
    offer_delivery_charge = models.PositiveBigIntegerField(default=0)
    offer_caution_deposit = models.PositiveBigIntegerField(default=0)
    offer_total_charges = models.PositiveBigIntegerField(default=0)
    cancelled_rental=models.BooleanField(default=False)
    distance  = models.FloatField(default=0)

    STATUS_CHOICES = [
        ('confirmed','confirmed'),
        ('Taken', 'Taken'),
        ('Shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('rental_period','rental_period'),
        ('returned','returned'),
        ('cancelled','cancelled'),
        ('completed','completed'),
    ]

    PAYMENT_CHOICES = [
        ('paypal','paypal'),
        ('wallet','wallet'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    payment_choice=models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )
