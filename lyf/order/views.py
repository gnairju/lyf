from django.shortcuts import render, redirect
from django.contrib import messages
from .models import order
from cart.models import cart
from user.models import userAddress
from opencage.geocoder import OpenCageGeocode
from django.urls import reverse
from geopy.distance import geodesic
from adminPanel.models import Product

def get_coordinates_from_postal_code(postal_code):
    key = '632ebcb5bf224551955bab10f7b9974c'  # Replace with your OpenCage API key
    geocoder = OpenCageGeocode(key)

    results = geocoder.geocode(postal_code)

    if results and len(results):
        location = results[0]['geometry']
        return (location['lat'], location['lng'])
    else:
        return None

def calculate_distance(postal_code1, postal_code2):
    coords1 = get_coordinates_from_postal_code(postal_code1)
    coords2 = get_coordinates_from_postal_code(postal_code2)

    if coords1 and coords2:
        distance = geodesic(coords1, coords2).kilometers
        print(distance)
        return distance
    else:
        return None

def confirmRental(request):
    print('entered')
    if request.method == 'POST':
        address = request.POST.get('selected_address')
        add = userAddress.objects.get(id=address)
        user = request.user
        cart_instance = cart.objects.filter(user=user)
        print(cart_instance)
        x = add.pincode
        print(x)
        for i in cart_instance:
            y = i.product.pincodePro
            print(y)
            distance = calculate_distance(x, y)
            print(distance)
            if distance is not None and distance > 10:
                messages.error(request, 'Distance is too far. Order cannot be processed.')
                return redirect(reverse('cart:checkout'))
            else:

                total_price = i.product.price * i.quantity * i.days_needed
                order_instance = order.objects.create(
                    user=request.user,
                    address=add,
                    product=i.product,
                    quantity=i.quantity,
                    days_needed=i.days_needed,
                    total_price=total_price
                )
                c=Product.objects.get(id=i.product.id)
                c.quantity-=i.quantity
                c.save()
                if c.quantity<1:
                    c.is_active=False
                    c.save()
                cart_instance.delete()
            y=0
        print('Success')

    # Add the logic for rendering a confirmation page or redirecting to another view
    return redirect('home:homePage')
