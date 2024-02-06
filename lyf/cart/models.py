from django.db import models
from user.models import CustomUser
from adminPanel.models import Product
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.
class cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    days_needed=models.PositiveIntegerField(default=3)
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        verbose_name = "cart"

        
    def __str__(self) -> str:
        return self.user.first_name
    
