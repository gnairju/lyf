from django.shortcuts import render,redirect
from .models import order  # Assuming your Order model is in the same directory as this views file
from cart.models import cart  # Import the Cart model
from user.models import userAddress

def confirmRental(request):
    print('entered')
    if request.method == 'POST':
        address = request.POST.get('selected_address')
        add = userAddress.objects.get(id=address)
        print(add)
        user=request.user
        cart_instance = cart.objects.filter(user=user)
        print(cart_instance)

        for i in cart_instance:
            ord=order.objects.create(
                user=request.user,
                address=add,
                product = i.product,
                quantity=i.quantity,
                days_needed = i.days_needed,
            )
        cart_instance.delete()
        print('Success')
        
    # Add the logic for rendering a confirmation page or redirecting to another view

        return redirect('home:homePage')
