from django.shortcuts import render, get_object_or_404, redirect
from .models import cart
from adminPanel.models import Product
from django.contrib.auth.decorators import login_required
from user.models import CustomUser

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
    print(cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})


def checkout(request):
    if request.method == 'POST':
        # Retrieve the user's cart
        user_cart = cart.objects.filter(user=request.user)

        # Process the form data and calculate the total price
        total_price = 0
        for cart_item in user_cart:
            quantity = float(request.POST.get(f'quantity_{cart_item.id}', 0))
            days_required = float(request.POST.get(f'days_required_{cart_item.id}', 0))
            price = quantity * days_required * cart_item.product.price
            total_price += price
        print(price)
        print(total_price)
        # You can do something with the total_price, e.g., save it in the session
        request.session['total_price'] = total_price
        # Redirect to the next page
        context={
            'price':price,
            'total_price':total_price,
            'user_cart':user_cart
        }
        return render(request,'cart\checkout.html',context)

    # Render the checkout page if it's a GET request
    cart_items = cart.objects.filter(user=request.user)
    return render(request, 'cart\cart.html', {'cart_items':cart_items})