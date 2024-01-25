from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from order.models import order
from decimal import Decimal
from django.urls import reverse
from django.contrib import messages
from .models import user_wallet
from provider.models import provider_credentials
from user.views import performlogin


@login_required(login_url='user:performlogin')
def make_payments(request,id):
    PAYMENT_CHOICE=order.PAYMENT_CHOICES
    ord = order.objects.get(id=id)
    context={
        'ord':ord,
        'PAYMENT_CHOICE':PAYMENT_CHOICE
    }
    
    return render(request,'payments/payments.html',context)



@login_required(login_url='user:performlogin')
def payment_selection(request,id):
    ord=order.objects.get(id=id)
    PAYMENT_CHOICE=order.PAYMENT_CHOICES
    wall=user_wallet.objects.get(user=request.user)
    if request.method=='POST':
        payment_type=request.POST.get('payment_type')
        if payment_type=='paypal':
            return redirect('payments:final_pay',id=id)
        if payment_type=='wallet':
            if ord.total_charges>wall.balance_amount:
                messages.error(request,"Insufficient Balance")
            else:
                return redirect('payments:wallet_debit',id=id)
    context={'ord':ord,
             'wall':wall,
            'PAYMENT_CHOICE':PAYMENT_CHOICE,
            }
    return render(request,'payments/payments.html',context)


def final_pay(request,id):
    ord = order.objects.get(id=id)
    host = request.get_host()
    offer_total_charges_decimal = Decimal(str(ord.offer_total_charges)).quantize(Decimal('0.01'))


    paypal_dict={
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % offer_total_charges_decimal,
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


@login_required(login_url='user:performlogin')
def payment_done(request,id):
    ord=order.objects.get(id=id)
    ord.payment=True
    ord.save()
    messages.success(request,"payment done sucessfuly")
    return redirect('user:user_profile')


@login_required(login_url='user:performlogin')
def payment_cancelled(request):
    messages.error(request,"payment cancelled")
    return render(request,'user/user_payment.html')


def wallet_credit(request, id):
    ord = get_object_or_404(order, id=id)
    current_balance = user_wallet.objects.get(user=request.user).balance_amount
    amount = ord.total_charges
    new_balance = int(amount) + int(current_balance)

    # Assuming there is only one user_wallet object per user, otherwise, adjust accordingly
    user_wallet_obj, created = user_wallet.objects.get_or_create(user=request.user)
    user_wallet_obj.balance_amount = new_balance
    user_wallet_obj.save()
    ord.cancelled_rental=True
    ord.status='cancelled'
    ord.save()
    return redirect('user:user_profile')

@login_required(login_url='user:performlogin')
def wallet(request):
    user=request.user
    wall = get_object_or_404(user_wallet, user=user)
    print(wall)
    return render(request,'payments/wallet.html',{'wall':wall})


@login_required(login_url='user:performlogin')
def wallet_debit(request,id):
    wallet=user_wallet.objects.get(user=request.user)
    ord=order.objects.get(id=id)
    context={
        'ord':ord,
        'wallet':wallet,
    }
    if request.method=='POST':
        wallet.balance_amount=wallet.balance_amount-ord.offer_total_charges
        wallet.save()
        return redirect('payments:payment_done',id=id)

    return render(request,'payments/wallet_payment.html',context)


def provider_pay(request,id):
    ord = order.objects.get(id=id)
    product = ord.product
    host = request.get_host()
    total_price_decimal = Decimal(str(ord.total_price)).quantize(Decimal('0.01'))
    if product:
        pro=product.user
        if pro:
            provider=provider_credentials.objects.get(provider=pro)
    
    provider_mail=provider.paypal_id
    paypal_dict={
        'business': provider_mail,
        'amount': '%.2f' % total_price_decimal,
        'item_name' : 'order {}'.format(ord.id),
        'invoice':str(ord.id),
        'country_code':"USD",
        'notify_url' : 'https://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('adminPanel:pay_provider_success', kwargs={'id': ord.id})),
        'cancel_return': 'http://{}{}'.format(host,reverse('payments:payment_cancelled')),
        
    }

    
    form = PayPalPaymentsForm(initial=paypal_dict)
    context={
        'ord':ord,
        'form':form,
    }
    
    return render(request,'payments/provider_payment.html',context)