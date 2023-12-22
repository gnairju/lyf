from django.db import models
from user.models import CustomUser
# Create your models here.
from django.db import models

# Create your models here.
class Categories(models.Model):
    Name = models.CharField(max_length=50,null=False,unique=True)
    description = models.CharField(max_length=500,null=True)
    
    

    def __str__(self) -> str:
        return self.Name

class Product(models.Model):
    user = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    category=models.ForeignKey(Categories, related_name='products',on_delete=models.CASCADE)
    title  = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price=models.IntegerField()
    quantity=models.IntegerField()
    image=models.ImageField(upload_to='uploads/product_images/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

class multipleImage(models.Model):
    product=models.ForeignKey("adminPanel.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product_images/',blank=True,null=True)

    def __str__(self) -> str:
        return self.product.title