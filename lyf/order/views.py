from django.shortcuts import render
from .models import order  # Assuming your Order model is in the same directory as this views file
from cart.models import cart  # Import the Cart model

def confirmRental(request, id):
    print('entered')
    if request.method == 'POST':
        address = request.POST.get('selected_address')
        cart_instance = cart.objects.get(id=id)

        ord=order.objects.create(
            user=request.user,
            address=address,
            cart=cart_instance,
        )
        print('Success')

    # Add the logic for rendering a confirmation page or redirecting to another view

    return render(request, 'test.html')
