from django.contrib import admin

# Register your models here.
from .models import Categories, Product, multipleImage

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(multipleImage)