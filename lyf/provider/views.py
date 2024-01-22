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


@login_required(login_url='user:performlogin')
def providerPanel(request):
    product=Product.objects.all()
    return render(request,'provider/providerPanel.html',{'product':product})


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

    return render(request, 'provider/providerAddProducts.html', {'categories': categories})


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
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image') if 'image' in request.FILES else None
        pincodePro = request.POST.get('pincodePro')
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
    ord = order.objects.filter(product__user=request.user)
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
    ord.product.quantity+=1
    print(ord.product.quantity)
    if ord.product.is_active==False:
        ord.product.is_active=True
    ord.save()
    print(ord.product.quantity)
    return redirect(reverse('provider:providerApproval'))

@login_required(login_url='user:performlogin')
def provider_details(request):
    provider_instance_set=None
    try:
        provider_instance_set = get_object_or_404(provider_credentials, provider=request.user)
        print(provider_instance_set)
    except:
        provider_instance_set=None

    if request.method == 'POST':
        pan_number = request.POST.get('pan_number')
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
            return redirect('provider:provider_details')
        else:
            provider_credentials.objects.create(
                provider=request.user,
                pan_card=pan_number,
                pan_photo=pan_image,
                paypal_id=paypal_mail,
            )
            return redirect('provider:provider_details')


    return render(request, 'provider/provider_details.html', {'provider_instance_set': provider_instance_set})
