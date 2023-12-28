from django.urls import path
from . import views

app_name='order'
urlpatterns = [
    path('confirmRental/<int:id>', views.confirmRental,name='confirmRental'),
]
