from django.urls import path
from . import views


app_name='order'
urlpatterns = [
    path('confirmRental', views.confirmRental,name='confirmRental'),
    path('rental_management/',views.rental_management,name='rental_management'),
    path('statusChange/<int:id>/',views.statusChange,name='statusChange'),
    path('coupon_apply/<int:id>',views.coupon_apply,name='coupon_apply'),
    path('coupon_clear/<int:id>',views.coupon_clear,name='coupon_clear'),
]
