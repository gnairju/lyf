from django.urls import path
from . import views
from paypal.standard.ipn import views as paypal_ipn_views

app_name='payments'
urlpatterns = [
    path('payments/<int:id>',views.make_payments,name='make_payments'),
    path('payment_done/<int:id>',views.payment_done,name='payment_done'),
    path('payment_cancelled',views.payment_cancelled,name='payment_cancelled'),
    path('make_payments/<int:id>/',views.make_payments,name='make_payments'),
    path('final_pay/<int:id>',views.final_pay,name='final_pay'),
    path('wallet',views.wallet,name='wallet'),
    path('wallet_credit/<int:id>/',views.wallet_credit,name='wallet_credit'),
    path('payment_selection/<int:id>',views.payment_selection,name='payment_selection'),
    path('wallet_debit/<int:id>',views.wallet_debit,name='wallet_debit'),
    path('provider_pay/<int:id>/', views.provider_pay, name='provider_pay'),
]
