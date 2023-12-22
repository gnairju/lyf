from django.urls import path
from . import views

app_name='user'
urlpatterns = [
    path('performlogin', views.performlogin,name='performlogin'),
    path('user_registration', views.user_registration,name='user_registration'),
    path('otpPage',views.otpPage,name='otpPage'),
    path('perform_logout',views.perform_logout,name='perform_logout'),
    path('resendOtp',views.resendOtp,name='resendOtp'),
]
