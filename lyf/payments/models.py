from django.db import models
from user.models import CustomUser

# Create your models here.
class user_wallet(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance_amount=models.PositiveBigIntegerField(default=0)
    updated_at=models.DateTimeField(auto_now=True)


    

    