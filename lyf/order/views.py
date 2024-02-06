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
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from user.views import performlogin
from adminPanel.views import admin_access_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_coordinates_from_postal_code(postal_code):
    key = '632ebcb5bf224551955bab10f7b9974c'  #OpenCage API key
    geocoder = OpenCageGeocode(key)

    results = geocoder.geocode(postal_code)

    if results and len(results):
        location = results[0]['geometry']
        return (location['lat'], location['lng'])
    else:
        return None
    

def calculate_platform_fee(total_price):
    x=total_price/100
    if x>30:
        return 30
    else:
        return x 


def calculate_distance(postal_code1, postal_code2):
    coords1 = get_coordinates_from_postal_code(postal_code1)
    coords2 = get_coordinates_from_postal_code(postal_code2)

    if coords1 and coords2:
        distance = geodesic(coords1, coords2).kilometers
        return distance
    else:
        return None
    
@login_required(login_url='user:performlogin')
def confirmRental(request):
    if request.method == 'POST':
        address = request.POST.get('selected_address')
        add = userAddress.objects.get(id=address)
        print(add)
        present_user = request.user
        cart_instance = cart.objects.filter(user=present_user)
        x = add.pincode
        print(x)
        print(type(x))
        for i in cart_instance:
            y = i.product.pincodePro
            print(y)
            print(type(y))
            distance = calculate_distance(x, y)
            print(distance)
            if distance is not None and distance > 10:
                messages.error(request, 'Distance is too far. Order cannot be processed.')
                return redirect(reverse('cart:checkout'))
            else:
                if i.product.discounted_price:
                    total_price = i.product.discounted_price * i.quantity * i.days_needed
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
                    from_date=i.from_date,
                    to_date=i.to_date,
                    total_price=total_price,
                    platform_charges=platform_charges,
                    caution_deposit = security,
                    total_charges=total_charges,
                    distance=distance,
                )
                # c=Product.objects.get(id=i.product.id)
                # c.quantity-=i.quantity
                # c.save()
                # if c.quantity<1:
                #     c.rentable=False
                #     c.save()
                cart_instance.delete()
            y=0
        print('Success')

    # Add the logic for rendering a confirmation page or redirecting to another view
    messages.success(request,'Your request has been send to provider side.')
    return redirect('home:homePage')


@admin_access_required
def rental_management(request):
    ord=order.objects.all().order_by('-date')
    ord_per_page=10
    paginator = Paginator(ord,ord_per_page)

    page = request.GET.get('page')
    try:
        ord = paginator.page(page)
    except PageNotAnInteger:
        ord = paginator.page(1)
    except EmptyPage:
        ord = paginator.page(paginator.num_pages)
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
        messages.success(request,'Status changed')
    return redirect('order:rental_management')


def coupon_apply(request, id):
    order_instance = order.objects.get(id=id)

    if request.method == 'POST':
        cop_code = request.POST.get('coupons')
        print(cop_code)

        try:
            coupon = coupons.objects.get(name=cop_code)
            coupon_type = coupon.coupon_type
            discount_percentage = coupon.discount
            if coupon.is_active:
                if coupon_type == 'delivery':
                    print('delivery')
                    delivery_charge = order_instance.delivery_charge
                    discount_amount = (discount_percentage / 100) * delivery_charge
                    order_instance.offer_delivery_charge = delivery_charge - discount_amount
                    order_instance.offer_caution_deposit = order_instance.caution_deposit
                    order_instance.offer_total_price=order_instance.total_price

                elif coupon_type == 'caution':
                    print('caution')
                    caution_deposit = order_instance.caution_deposit
                    discount_amount = (discount_percentage / 100) * caution_deposit
                    order_instance.offer_caution_deposit = caution_deposit - discount_amount
                    order_instance.offer_delivery_charge=order_instance.delivery_charge
                    order_instance.offer_total_price=order_instance.total_price

                elif coupon_type == 'Total':
                    print('total')
                    total_price = order_instance.total_price
                    discount_amount = (discount_percentage / 100) * total_price
                    order_instance.offer_total_charges = total_price - discount_amount
                    order_instance.offer_delivery_charge=order_instance.delivery_charge
                    order_instance.offer_caution_deposit = order_instance.caution_deposit

                order_instance.offer_total_charges = order_instance.offer_delivery_charge + order_instance.offer_caution_deposit + order_instance.offer_total_price + order_instance.platform_charges
                print(order_instance.offer_total_charges)

                # Assign the new coupon
                order_instance.coupon = coupon
                coupon.num -= 1
                if coupon.num == 1:
                    coupon.is_active = False
                coupon.save()
                order_instance.save()
                messages.success(request,'Coupon successfully')
            else:
                messages.error(request,'Invalid coupon')

        except coupons.DoesNotExist:
            messages.error(request, 'Invalid coupon')
            return HttpResponseServerError("Internal Server Error")

    return redirect('payments:make_payments', id=id)


def coupon_clear(request, id):
    ord = order.objects.get(id=id)
    ord.coupon = None
    ord.save()
    next_url = reverse('payments:make_payments', kwargs={'id': id})

    return redirect(next_url)