from django.shortcuts import get_object_or_404
from django.db import models
from user.models import CustomUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import datetime

# Create your models here.
class Categories(models.Model):
    Name = models.CharField(max_length=50,null=False,unique=True)
    description = models.CharField(max_length=500,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.Name

class Product(models.Model):
    phone_number_validator = RegexValidator(
        regex=r'^\d{1,15}$',  # This regex allows 1 to 15 digits
        message='Phone number must contain only digits.',
        code='invalid_phone_number'
    )
    user = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    category=models.ForeignKey(Categories, related_name='products',on_delete=models.CASCADE)
    title  = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price=models.IntegerField()
    discounted_price=models.IntegerField(default=0)
    security=models.IntegerField()
    quantity=models.PositiveIntegerField()
    image=models.ImageField(upload_to='uploads/product_images/',blank=True,null=True)
    pincodePro=models.CharField(max_length=20)
    address = models.CharField(max_length=50,null=False)
    street = models.CharField(max_length=50,null=False)
    phone = models.CharField(max_length=20,blank=True,
        null=True,
        validators=[phone_number_validator])
    city = models.CharField(max_length=20)
    state= models.CharField(max_length=50,null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    availability=models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    rentable = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    
    
    # def get_discounted_price(self):
    #     print('helloooo')
    #     current_date = timezone.now().date()

    #     category_offer = CategoryOffer.objects.filter(
    #         category=self.category,
    #         start_date__lte=current_date,
    #         end_date__gte=current_date,
    #         is_active=True
    #     ).first()

    #     product_offer = ProductOffer.objects.filter(
    #         product=self,
    #         start_date__lte=current_date,
    #         end_date__gte=current_date,
    #         is_active=True
    #     ).first()

    #     if category_offer and product_offer:
    #         if product_offer.discount_percentage > category_offer.discount_percentage:
    #             self.discounted_priceprice = self.price - (self.price * product_offer.discount_percentage / 100)
    #         else:
    #             self.discounted_priceprice = self.price - (self.price * category_offer.discount_percentage / 100)
    #     elif category_offer:
    #         self.discounted_priceprice = self.price - (self.price * category_offer.discount_percentage / 100)
    #     elif product_offer:
    #         self.discounted_priceprice = self.price - (self.price * product_offer.discount_percentage / 100)
    #     else:
    #          return self.price


class multipleImage(models.Model):
    product=models.ForeignKey("adminPanel.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product_images/',blank=True,null=True)

    def __str__(self) -> str:
        return self.product.title
    
    
class coupons(models.Model):
    name=models.CharField(max_length=30,null=False)
    num=models.BigIntegerField(default=25)
    COUPON_CHOICE = [
        ('delivery','delivery'),
        ('caution','caution'),
        ('Total','Total'),
    ]
    coupon_type=models.CharField(max_length=30, choices=COUPON_CHOICE, blank=True)
    discount=models.FloatField(null=False)
    created=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    

class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(ProductOffer, self).save(*args, **kwargs)
        product = get_object_or_404(Product, id=self.product.id)

        if product.is_active:
            new_product_discount_price = product.price * (1 - (int(self.discount_percentage) / 100))
            if product.discounted_price != new_product_discount_price:
                product.discounted_price = new_product_discount_price
                product.save()

        if not self.is_active or (self.end_date and datetime.now().date() > self.end_date):
            product.discounted_price = Decimal(0)
            product.save()


class CategoryOffer(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(100)],)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(CategoryOffer, self).save(*args, **kwargs)
        category = get_object_or_404(Categories, id=self.category.id)
        print(self.discount_percentage)
        x = self.discount_percentage
        print(type(x))
        if category.is_active:
            products = Product.objects.filter(category__id=category.id)

            for product in products:
                new_product_discount_price = product.price * (
                    1 - (int(self.discount_percentage) / 100)
                )
                if product.discounted_price != new_product_discount_price:
                    product.discounted_price = new_product_discount_price
                    product.save()

        if not self.is_active  or (self.end_date and datetime.now().date() > self.end_date):
            products = Product.objects.filter(category=self.category)
            for product in products:
                product.discount_price = Decimal(0)
                product.save()

                