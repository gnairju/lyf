from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('', views.homePage,name='homePage'),
    path('searchbar',views.searchbar,name='searchbar'),
    path('contactus',views.contactus,name='contactus'),
] 