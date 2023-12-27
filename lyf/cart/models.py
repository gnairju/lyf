from django.db import models
from user.models import CustomUser
from adminPanel.models import Product
# Create your models here.
class cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    days_needed=models.PositiveIntegerField(default=3)
    

    class Meta:
        verbose_name = "cart"


