from django.urls import path
from . import views

app_name='user'
urlpatterns = [
    path('performlogin', views.performlogin,name='performlogin'),
    path('user_registration', views.user_registration,name='user_registration'),
    path('otpPage',views.otpPage,name='otpPage'),
    path('perform_logout',views.perform_logout,name='perform_logout'),
    path('resendOtp',views.resendOtp,name='resendOtp'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_payment',views.user_payment,name='user_payment'),
    path('user_cancel_rental/<int:id>',views.user_cancel_rental,name='user_cancel_rental'),
]
