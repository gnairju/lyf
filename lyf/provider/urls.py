from django.urls import path
from . import views

app_name='provider'
urlpatterns = [
    path('providerPanel/', views.providerPanel,name='providerPanel'),
    path('providerAddProducts',views.providerAddProduct,name='providerAddProducts'),
    path('providerUpdateProducts/<int:id>',views.providerUpdateProducts,name='providerUpdateProducts'),
    path('providerDeleteProducts/<int:id>',views.providerDeleteProducts,name='providerDeleteProducts'),
    path('providerApproval',views.providerApproval,name='providerApproval'),
    path('activateOrder/<int:id>',views.activateOrder,name='activateOrder'),  
    path('deleteOrder/<int:id>',views.deleteOrder,name='deleteOrder'),
    path('provider_details/',views.provider_details,name='provider_details'),
    path('reactivate_product/<int:id>',views.reactivate_product,name='reactivate_product'),
    path('cancelOrder/<int:id>',views.cancelOrder,name='cancelOrder'),

]
