from django.urls import path
from . import views

app_name='cart'
urlpatterns = [
    path('addToCart/<int:id>', views.addToCart,name='addToCart'),
    path('cartPage',views.cartPage,name='cartPage'),
    path('removeItemCart/<int:id>', views.removeItemCart,name='removeItemCart'),
    path('checkout',views.checkout,name='checkout'),
    path('addAddress',views.addAddress,name='addAddress'),
    path('delete_user_address/<int:id>', views.deleteUserAddress, name='deleteUserAddress'),
]
