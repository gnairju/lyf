from django.db import models
from adminPanel.models import Product
from user.models import CustomUser

# Create your models here.

class provider_details(models.Model):
    provider=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    provider_pan=models.CharField(max_length=30,null=False)
    pan_img=models.ImageField(null=False)
    paypal_email=models.EmailField(null=False)
    