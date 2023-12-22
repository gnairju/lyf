from django.urls import path
from . import views

app_name='products'
urlpatterns = [
    path('productPage/<int:id>', views.productPage,name='productPage'),
]
