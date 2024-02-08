from django.shortcuts import render,redirect
from adminPanel.models import Categories
from adminPanel.models import Product
from user.views import performlogin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from adminPanel.models import multipleImage
from django.core.mail import send_mail
from user.models import CustomUser
from django import http
from order.models import order
from .models import provider_credentials
from adminPanel.models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required(login_url='user:performlogin')
def providerPanel(request):
    user=request.user
    try:
        pro_cred=provider_credentials.objects.get(provider=user)
        if pro_cred:
            product=Product.objects.all()
            return render(request,'provider/providerPanel.html',{'product':product})
    except:
        messages.error(request,'Please add your details')
        return redirect('provider:provider_details')


def create_security(given_price):
    price = int(given_price)
    if price>100:
        x=price*5
        return x
    else:
        x=price*10
        return x


@login_required(login_url='user:performlogin')
def providerAddProduct(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_Name = request.POST.get('category')
        quantity = request.POST.get('quantity')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincodePro = request.POST.get('pincodePro')

        # Handle main image upload
        main_image = request.FILES.get('image') if 'image' in request.FILES else None

        # Handle multiple images upload
        additional_images = request.FILES.getlist('images')

        # Assuming you have a Categories model with an id field
        category = Categories.objects.get(Name=category_Name)

        security=create_security(price)
        # Create the product
        product = Product.objects.create(
            user=request.user,
            category=category,
            title=title,
            description=description,
            price=price,
            image=main_image,
            quantity=quantity,
            pincodePro = pincodePro,
            phone = phone,
            address = address,
            street = street,
            city = city,
            state = state,
            security = security,
        )

        # Create MultipleImage instances for additional images
        for img in additional_images:
            multipleImage.objects.create(product=product, image=img)

        user = request.user
        if user.is_staff == False:
            user.is_staff = True
            user.save()
        
        
        return redirect('provider:providerPanel')  # Redirect to the provider panel after adding a product

    # Fetch categories from the database
    categories = Categories.objects.all()

    return render(request, 'provider/providerAddproducts.html', {'categories': categories})
    return render(request, 'provider/providerAddproducts.html', {'categories': categories})


@login_required(login_url='user:performlogin')
def providerDeleteProducts(request,id):
    pro=Product.objects.get(id=id)
    pro.delete()
    return redirect('provider:providerPanel')


@login_required(login_url='user:performlogin')
def providerUpdateProducts(request, id):
    # Get the product instance using the product_id
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        # Process the form submission
        title = request.POST.get('title').strip()
        description = request.POST.get('description').strip()
        price = request.POST.get('price').strip()
        image = request.FILES.get('image') if 'image' in request.FILES else None
        pincodePro = request.POST.get('pincodePro').strip()
        # Update the product fields
        product.title = title
        product.description = description
        product.price = price
        product.pincodePro = pincodePro

        if image:
            product.image = image

        product.save()
        
        return redirect('provider:providerPanel')  # Redirect to the provider panel or any other desired page

    return render(request, 'provider/providerUpdateProducts.html', {'product': product})


@login_required(login_url='user:performlogin')
def providerApproval(request):
    ord = order.objects.filter(product__user=request.user).order_by('-date')
    #total_price = ord.product.price * ord.quantity * ord.days_needed
    context={
        'ord':ord
    }
    return render(request, 'provider/providerApproval.html', context)


@login_required(login_url='user:performlogin')
def activateOrder(request,id):
    ord = order.objects.get(id=id)
    ord.is_active=True
    subject = 'Rental Confirmation'
    message = f'Rental Confirmed for "{ord.product}". Please login to your user profile to make payments.'
    from_email = 'o23211671@gmail.com'  
    email = ord.user
    send_mail(subject, message, from_email, [email])
    ord.status='confirmed'
    ord.save()
    return redirect(reverse('provider:providerApproval'))


@login_required(login_url='user:performlogin')
def deleteOrder(request,id):
    ord = order.objects.get(id=id)
    ord.delete()
    return redirect(reverse('provider:providerApproval'))


@login_required(login_url='user:performlogin')
def reactivate_product(request,id):
    ord=order.objects.get(id=id)
    quan=ord.quantity
    pro=ord.product.id
    product_instance=Product.objects.get(id=pro)
    product_instance.quantity += quan
    product_instance.save()
    if product_instance.rentable==False:
        product_instance.rentable=True
    product_instance.save()
    ord.status='completed'
    ord.save()
    print(product_instance.quantity)
    print(product_instance.rentable)
    return redirect('provider:providerApproval')


@login_required(login_url='user:performlogin')
def provider_details(request):
    provider_instance_set=None
    try:
        provider_instance_set = get_object_or_404(provider_credentials, provider=request.user)
        print(provider_instance_set)
    except:
        provider_instance_set=None

    if request.method == 'POST':
        pan_number = request.POST.get('pan_number').strip()
        pan_image = request.FILES.get('pan_image') if 'pan_image' in request.FILES else None
        paypal_mail = request.POST.get('paypal_mail')
        print(pan_image)


        if provider_instance_set:
            provider_instance_set.pan_card = pan_number
            provider_instance_set.pan_photo = pan_image
            provider_instance_set.paypal_id = paypal_mail

            if pan_image:
                provider_instance_set.pan_photo=pan_image
            provider_instance_set.save()
            messages.success(request,'Provider details updated')

            return redirect('provider:provider_details')
        else:
            provider_credentials.objects.create(
                provider=request.user,
                pan_card=pan_number,
                pan_photo=pan_image,
                paypal_id=paypal_mail,
            )
            messages.success(request,'Provider details added')
            return redirect('provider:provider_details')


    return render(request, 'provider/provider_details.html', {'provider_instance_set': provider_instance_set})


def cancelOrder(request,id):
    ord=order.objects.get(id=id)
    ord.status='cancelled'
    ord.save()
    return redirect('provider:providerApproval')


def provider_payments(request):
    user = request.user
    ord = order.objects.filter(product__user=user, payment_provider=True)
    return render(request,'provider/provider_payments.html',{'ord':ord})