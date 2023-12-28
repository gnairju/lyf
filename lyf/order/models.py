from django.db import models
from cart.models import cart
from user.models import CustomUser,userAddress
from adminPanel.models import Product
from datetime import datetime

class order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address = models.ForeignKey(userAddress,on_delete=models.CASCADE)
    cart = models.ForeignKey(cart,on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)


