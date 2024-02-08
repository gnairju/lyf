from django.shortcuts import render, get_object_or_404, redirect
from .models import cart
from adminPanel.models import Product
from django.contrib.auth.decorators import login_required
from user.models import CustomUser,userAddress
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from order.models import order


# @login_required(login_url='user:performlogin')
# def updateCart(request):
#     if request.method == 'POST':
#         today = datetime.now().date()

#         for cart_item in cart.objects.filter(user=request.user):
#             quantity_key = f'quantity_{cart_item.id}'
#             from_date_key = f'from_date_{cart_item.id}'
#             to_date_key = f'to_date_{cart_item.id}'
#             # days_needed_key = f'days_needed_{cart_item.id}'

#             try:
#                 quantity = int(request.POST.get(quantity_key))
#                 cart_item.quantity = quantity
#             except ValueError:
#                 cart_item.delete()

#             try:
#                 from_date_str = request.POST.get(from_date_key)
#                 from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
#                 if from_date < today:
#                     messages.error(request, 'Please provide a valid "from" date')
#                 else:
#                     cart_item.from_date = from_date
#                     cart_item.save()
#             except ValueError:
#                 return redirect('cart:cartPage')

#             try:
#                 to_date_str = request.POST.get(to_date_key)
#                 to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()
#                 if to_date < today:
#                     messages.error(request, 'Please provide a valid "to" date')
#                 else:
#                     cart_item.to_date = to_date
#                     cart_item.save()
#             except ValueError:
#                 return redirect('cart:cartPage')

#         # Save changes to the cart items outside the loop
#         cart_item.save()

#     return redirect('cart:cartPage')

@login_required(login_url='user:performlogin')
def updateCart(request):
    if request.method == 'POST':
        today = timezone.now().date()

        for cart_item in cart.objects.filter(user=request.user):
            quantity_key = f'quantity_{cart_item.id}'
            from_date_key = f'from_date_{cart_item.id}'
            to_date_key = f'to_date_{cart_item.id}'

            if quantity_key in request.POST:
                quantity = int(request.POST.get(quantity_key))
                cart_item.quantity = quantity

                if cart_item.quantity > cart_item.product.quantity:
                    messages.error(request, 'Product not available')
                    return redirect(reverse('cart:cartPage'))
                else:
                    cart_item.save()

            if from_date_key in request.POST:
                from_date_str = request.POST.get(from_date_key)
                if from_date_str:
                    from_date = timezone.make_aware(timezone.datetime.strptime(from_date_str, "%Y-%m-%d"))
                    if from_date.date() < today:
                        messages.error(request, 'Please provide a valid from date')
                        return redirect(reverse('cart:cartPage'))
                    elif (from_date.date() - today).days < 1:
                        messages.error(request, 'Your from date should be after one day')
                        return redirect(reverse('cart:cartPage'))
                    else:
                        cart_item.from_date = from_date

            if to_date_key in request.POST:
                to_date_str = request.POST.get(to_date_key)
                if to_date_str:
                    to_date = timezone.make_aware(timezone.datetime.strptime(to_date_str, "%Y-%m-%d"))
                    if to_date.date() < cart_item.from_date.date():
                        messages.error(request, 'Please provide a valid to date')
                        return redirect(reverse('cart:cartPage'))
                    elif (to_date.date() - cart_item.from_date.date()).days < 2:
                        messages.error(request, 'There should be at least 2 days rental')
                        return redirect(reverse('cart:cartPage'))
                    else:
                        cart_item.to_date = to_date
            cart_item.save()

            # if cart_item.from_date and cart_item.to_date:
            #     print('Hello')
            #     overlapping_bookings = order.objects.filter(
            #         product=cart_item.product,
            #         from_date__lte=cart_item.to_date,
            #         to_date__gte=cart_item.from_date,
            #     ).exclude(id=cart_item.id)
            #     print(overlapping_bookings)
            #     if overlapping_bookings.exists():
            #         messages.error(request, 'This product is already booked for the selected dates')
            #         return redirect(reverse('cart:cartPage'))

            # cart_item.save()

    return redirect('cart:cartPage')




def addToCart(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            cart_items = cart.objects.filter(user=request.user)

            cart_item, created = cart.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 1,'from_date': timezone.now()+timedelta(days=1),
                    'to_date': timezone.now() + timedelta(days=3)}
            )

            if not created:
                if product.quantity>1:
                    print(product.quantity)
                    cart_item.quantity += 1
                    defaults={'from_date': timezone.now() + timedelta(days=1),
                        'to_date': timezone.now() + timedelta(days=3)}
                    cart_item.save()
            cart_items = cart.objects.filter(user=request.user)
            return render(request, 'cart/cart.html', {'cart_items': cart_items})
        else:
            return redirect('user:performlogin')
    
    return render(request,'cart/cart.html')


@login_required(login_url='user:performlogin')
def cartPage(request):
    user = CustomUser.objects.get(id=request.user.id)  
    cart_items = cart.objects.filter(user=user)
    total_price = 0

    for cart_item in cart_items:
        quantity = float(request.POST.get(f'quantity_{cart_item.id}', 0))
        days_required = float(request.POST.get(f'days_required_{cart_item.id}', 0))
        if cart_item.product.discounted_price>0:
            total_price += quantity * days_required * cart_item.product.discounted_price
        else:
            total_price += quantity * days_required * cart_item.product.price

    

    request.session['total_price'] = total_price

    address=userAddress.objects.filter(user=request.user)
    context={
            'total_price':total_price,
            'cart_items':cart_items,
            'address':address
    }
    return render(request, 'cart/cart.html', context)


def removeItemCart(request,id):
    citem=cart.objects.get(id=id)
    citem.delete()
    return redirect('cart:cartPage')


@login_required(login_url='user:performlogin')
def checkout(request):
    cart_items = cart.objects.filter(user=request.user)
    address = userAddress.objects.filter(user=request.user)

    for cart_item in cart_items:
        if cart_item.from_date and cart_item.to_date:
            overlapping_bookings = order.objects.filter(
                product=cart_item.product,
                from_date__lte=cart_item.to_date,
                to_date__gte=cart_item.from_date,
            ).exclude(id=cart_item.id)

            if overlapping_bookings.exists():
                messages.error(request, 'This product is already booked for the selected dates')
                return redirect(reverse('cart:cartPage'))

            if cart_item.from_date >= cart_item.to_date:
                messages.error(request, 'Invalid date range for product')
                return redirect(reverse('cart:cartPage'))
            

    return render(request, 'cart/checkout.html', {'address': address})


@never_cache
def addAddress(request):
    if request.method=='POST':
        addressType = request.POST.get('addressType').strip()
        firstname = request.POST.get('firstname').strip()
        lastname = request.POST.get('lastname').strip()
        address = request.POST.get('address').strip()
        street = request.POST.get('street').strip()
        phone = request.POST.get('phone').strip()
        pincode = request.POST.get('pincode').strip()
        city = request.POST.get('city').strip()
        state = request.POST.get('state').strip()

        userAddress.objects.create(
            addressType=addressType,
            firstname=firstname,
            lastname=lastname,
            address=address,
            street=street,
            phone=phone,
            pincode=pincode,
            city=city,
            state=state,
            user=request.user  # Assuming you have a user associated with the address
        )
        return redirect('cart:checkout')
    return render(request,'cart/addAddress.html')



@never_cache
def deleteUserAddress(request, id):
    # Use get_object_or_404 to retrieve the object or return a 404 response
    add = get_object_or_404(userAddress, id=id)
    add.delete()
    return redirect('cart:checkout')

