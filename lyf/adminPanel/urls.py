
from django.urls import path
from . import views

app_name='adminPanel'
urlpatterns = [
    path('adminPanel', views.adminPanel, name='adminPanel'),
    path('adminProducts',views.adminProducts,name='adminProducts'),
    path('adminCategory',views.adminCategory,name='adminCategory'),
    path('adminAddCategory',views.adminAddCategory,name='adminAddCategory'),
    path('adminUpdateCategory/<int:id>',views.adminUpdateCategory,name='adminUpdateCategory'),
    path('adminDeleteCategory/<int:id>',views.adminDeleteCategory,name='adminDeleteCategory'),
    path('providerList',views.providerList,name='providerList'),
    path('renterList',views.renterList,name='renterList'),
    path('blockUnblockUserProvider/<int:id>',views.blockUnblockUserProvider,name='blockUnblockUserProvider'),
    path('blockUnblockUserRenter/<int:id>',views.blockUnblockUserRenter,name='blockUnblockUserRenter'),
    path('adminProducts',views.adminProducts,name='adminProducts'),
    path('activeDeactiveProducts/<int:id>',views.activeDeactiveProducts,name='activeDeactiveProducts'),
]
