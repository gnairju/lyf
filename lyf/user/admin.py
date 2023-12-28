from django.contrib import admin
from .models import CustomUser,userAddress
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(userAddress)