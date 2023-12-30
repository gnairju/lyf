from django.urls import path
from . import views

app_name='order'
urlpatterns = [
    path('confirmRental', views.confirmRental,name='confirmRental'),
]
