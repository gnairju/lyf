from django.shortcuts import render, get_object_or_404, redirect
from .models import cart
from adminPanel.models import Product
from django.contrib.auth.decorators import login_required
from user.models import CustomUser,userAddress
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, redirect


def addToCart(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)

            # Fetch all cart items for the user
            cart_items = cart.objects.filter(user=request.user)

            # Get the cart item for the selected product or create a new one
            cart_item, created = cart.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 1}  # Set the default quantity if the item is newly created
            )

            # Update the quantity if the item already exists in the cart
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            # Fetch all cart items for the user after the update
            cart_items = cart.objects.filter(user=request.user)


            return render(request, 'cart/cart.html', {'cart_items': cart_items})
        else:
            return redirect('user:performlogin')
        



def removeItemCart(request,id):
    citem=cart.objects.get(id=id)
    citem.delete()
    return redirect('cart:cartPage')


@login_required(login_url='user:performlogin')
def cartPage(request):
    user = CustomUser.objects.get(id=request.user.id)  # Assuming user.id is the primary key
    cart_items = cart.objects.filter(user=user)
    total_price = 0

    for cart_item in cart_items:
        quantity = float(request.POST.get(f'quantity_{cart_item.id}', 0))
        days_required = float(request.POST.get(f'days_required_{cart_item.id}', 0))
        price = quantity * days_required * cart_item.product.price
        total_price += price
    

    request.session['total_price'] = total_price

    address=userAddress.objects.filter(user=request.user)
    context={
            'price':price,
            'total_price':total_price,
            'cart_items':cart_items,
            'address':address
    }
    return render(request, 'cart/cart.html', context)



def checkout(request):
    address=userAddress.objects.filter(user=request.user)
    return render(request,'cart\checkout.html',{'address':address})


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

    # Delete the object
    add.delete()

    # Redirect to the checkout page
    return redirect('cart:checkout')
