from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from order.models import order
from decimal import Decimal
from django.urls import reverse
from django.contrib import messages

def make_payments(request,id):
    ord = order.objects.get(id=id)
    context={
        'ord':ord,
    }
    
    return render(request,'payments/payments.html',context)

def final_pay(request,id):
    ord = order.objects.get(id=id)
    host = request.get_host()
    total_charges_decimal = Decimal(str(ord.total_charges)).quantize(Decimal('0.01'))


    paypal_dict={
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % total_charges_decimal,
        'item_name' : 'order {}'.format(ord.id),
        'invoice':str(ord.id),
        'country_code':"USD",
        'notify_url' : 'https://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payments:payment_done', kwargs={'id': ord.id})),
        'cancel_return': 'http://{}{}'.format(host,reverse('payments:payment_cancelled')),
        
    }

    
    form = PayPalPaymentsForm(initial=paypal_dict)
    context={
        'ord':ord,
        'form':form,
    }
    
    return render(request,'payments/payment_paypal.html',context)

def payment_done(request,id):
    ord=order.objects.get(id=id)
    ord.payment=True
    ord.save()
    messages.success(request,"payment done")
    return render(request,'user/user_payment.html')

def payment_cancelled(request):
    messages.error(request,"payment cancelled")
    return render(request,'user/user_payment.html')

