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


def updateCart(request):
    if request.method == 'POST':
        for cart_item in cart.objects.filter(user=request.user):
            quantity_key = f'quantity_{cart_item.id}'
            days_needed_key = f'days_needed_{cart_item.id}'
            
            quantity = int(request.POST.get(quantity_key))
            days_needed = int(request.POST.get(days_needed_key))

            cart_item.quantity = quantity
            cart_item.days_needed = days_needed

            if cart_item.quantity > cart_item.product.quantity:
                messages.error(request, 'Product not available')
                return redirect(reverse('cart:cartPage'))
            else:
                cart_item.save()

    return redirect('cart:cartPage')


def addToCart(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            # quantity = request.POST.get('quantity')
            # days_needed = request.POST.get('days_needed')

            # Fetch all cart items for the user
            cart_items = cart.objects.filter(user=request.user)

            # Get the cart item for the selected product or create a new one
            cart_item, created = cart.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 1, 'days_needed': 3}
            )

            # Update the quantity if the item already exists in the cart
            if not created:
                cart_item.quantity += 1
                cart_item.days_needed = 3
                cart_item.save()
            
            # Fetch all cart items for the user after the update
            cart_items = cart.objects.filter(user=request.user)
            return render(request, 'cart/cart.html', {'cart_items': cart_items})
        else:
            return redirect('user:performlogin')
        


@login_required(login_url='user:performlogin')
def cartPage(request):
    user = CustomUser.objects.get(id=request.user.id)  # Assuming user.id is the primary key
    cart_items = cart.objects.filter(user=user)
    total_price = 0

    for cart_item in cart_items:
        quantity = float(request.POST.get(f'quantity_{cart_item.id}', 0))
        days_required = float(request.POST.get(f'days_required_{cart_item.id}', 0))
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



def checkout(request):
    address=userAddress.objects.filter(user=request.user)
    return render(request,'cart/checkout.html',{'address':address})


@never_cache
def addAddress(request):
    if request.method=='POST':
        addressType = request.POST.get('addressType')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        street = request.POST.get('street')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')

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

