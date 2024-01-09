from django.shortcuts import render, redirect
from django.contrib import messages
from .models import order
from cart.models import cart
from user.models import userAddress
from opencage.geocoder import OpenCageGeocode
from django.urls import reverse
from geopy.distance import geodesic
from adminPanel.models import Product
from datetime import datetime, timedelta
from adminPanel.models import coupons

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
    
def calculate_platform_fee(total_price):
    x=total_price/100
    if x>30:
        return 30
    else:
        return x 

def confirmRental(request):
    if request.method == 'POST':
        address = request.POST.get('selected_address')
        add = userAddress.objects.get(id=address)
        user = request.user
        cart_instance = cart.objects.filter(user=user)
        x = add.pincode
        for i in cart_instance:
            y = i.product.pincodePro
            distance = calculate_distance(x, y)
            if distance is not None and distance > 10:
                messages.error(request, 'Distance is too far. Order cannot be processed.')
                return redirect(reverse('cart:checkout'))
            else:

                total_price = i.product.price * i.quantity * i.days_needed
                security = i.product.security
                platform_charges = calculate_platform_fee(total_price)
                print(platform_charges)
                total_charges=total_price + int(40) + platform_charges + security
                print(total_charges)
                order_instance = order.objects.create(
                    user=request.user,
                    address=add,
                    product=i.product,
                    quantity=i.quantity,
                    days_needed=i.days_needed,
                    total_price=total_price,
                    platform_charges=platform_charges,
                    caution_deposit = security,
                    total_charges=total_charges,
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



def rental_management(request):
    ord=order.objects.all()
    return render(request,'adminPanel/adminRentalDetails.html',{'ord':ord})


def statusChange(request,id):
    if request.method=='POST':
        status=request.POST.get('status')
        ord=order.objects.get(id=id)
        days_req=ord.days_needed
        if status=='delivered':
            ord.del_date=datetime.now()
            ord.save()
        ord.ret_date=ord.del_date+timedelta(days=days_req)
        ord.status=status
        ord.save()
    return redirect('order:rental_management')

def coupon_apply(request, id):
    order_instance = order.objects.get(id=id)

    if request.method == 'POST':
        cop_code = request.POST.get('coupons')
        print(cop_code)

        # Clear existing coupon
        if order_instance.coupon is not None:
            # c_type = order_instance.coupon.coupon_type
            # print(c_type)
            # order_instance.coupon = None
            # dis_amount = request.session.pop('dis_amount', 0)

            # if c_type == 'delivery':
            #     order_instance.delivery_charge += dis_amount
            # elif c_type == 'caution':
            #     order_instance.caution_deposit += dis_amount
            # elif c_type == 'Total':
            #     order_instance.total_charges += dis_amount

            # order_instance.save()
            messages.error(request,'A coupon already applied')
        else:
            try:
                coupon = coupons.objects.get(name=cop_code)
                coupon_type = coupon.coupon_type
                discount_percentage = coupon.discount

                if coupon_type == 'delivery':
                    print('delivery')
                    delivery_charge = order_instance.delivery_charge
                    discount_amount = (discount_percentage / 100) * delivery_charge
                    order_instance.delivery_charge -= discount_amount

                elif coupon_type == 'caution':
                    print('caution')
                    caution_deposit = order_instance.caution_deposit
                    discount_amount = (discount_percentage / 100) * caution_deposit
                    order_instance.caution_deposit -= discount_amount

                elif coupon_type == 'Total':
                    print('total')
                    total_charges = order_instance.total_charges
                    discount_amount = (discount_percentage / 100) * total_charges
                    order_instance.total_charges -= discount_amount

                # Assign the new coupon
                order_instance.coupon = coupon
                coupon.num-=1
                if coupon.quantity == 1:
                    coupon.is_active = False
                coupon.save()

                # Store the discount amount in the session
                request.session['dis_amount'] = discount_amount
                print(discount_amount)

                # Recalculate total_charges based on updated values
                order_instance.total_charges = (
                    order_instance.delivery_charge +
                    order_instance.caution_deposit +
                    order_instance.total_price
                )

                order_instance.save()

                # Explicitly delete the session variable
                del request.session['dis_amount']

            except coupons.DoesNotExist:
                messages.error(request, 'Invalid coupon')

    return redirect('payments:make_payments', id=id)
