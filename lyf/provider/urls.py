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
]
