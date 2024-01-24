from django.contrib import admin

# Register your models here.
from .models import Categories, Product, multipleImage, coupons, ProductOffer, CategoryOffer

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(multipleImage)
admin.site.register(coupons)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
