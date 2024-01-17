
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
    path('coupons_page',views.coupons_page,name='coupons_page'),
    path('add_coupons',views.add_coupons,name='add_coupons'),
    path('coupons_activate_deactivate/<int:id>',views.coupons_activate_deactivate,name='coupons_activate_deactivate'),
    path('pay_provider_success/<int:id>',views.pay_provider_success,name='pay_provider_success'),
    path('user_offers',views.user_offers,name='user_offers'),
    path('download_detailed_report',views.download_detailed_report,name='download_detailed_report'),
    path('report_download',views.report_download,name='report_download'),
]
