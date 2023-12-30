from django.db import models
from cart.models import cart
from user.models import CustomUser,userAddress
from adminPanel.models import Product
from datetime import datetime

class order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address = models.ForeignKey(userAddress,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    days_needed=models.PositiveIntegerField(default=3)
    date = models.DateField(default=datetime.now)
    is_active = models.BooleanField(default=False)
    