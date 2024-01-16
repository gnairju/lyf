from django.db import models
from adminPanel.models import Product
from user.models import CustomUser

# Create your models here.

class provider_credentials(models.Model):
    provider=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pan_card=models.CharField(max_length=35,null=False)
    pan_photo=models.ImageField(upload_to='uploads/provider/',blank=True,null=True)
    paypal_id=models.EmailField(null=False)
    
