from django.shortcuts import render,redirect
from adminPanel.models import Categories
from .models import Product
from django.contrib.auth.decorators import login_required
from user.views import performlogin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.http import HttpResponseBadRequest
from adminPanel.models import multipleImage
from django.core.mail import send_mail
from user.models import CustomUser
from django import http
from order.models import order
from adminPanel.models import Product
from user.models import CustomUser


@login_required(login_url='user:performlogin')
def providerPanel(request):
    product=Product.objects.all()
    return render(request,'provider/providerPanel.html',{'product':product})


@login_required(login_url='user:performlogin')
def providerAddProduct(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_Name = request.POST.get('category')
        quantity = request.POST.get('quantity')

        # Handle main image upload
        main_image = request.FILES.get('image') if 'image' in request.FILES else None

        # Handle multiple images upload
        additional_images = request.FILES.getlist('images')

        # Assuming you have a Categories model with an id field
        category = Categories.objects.get(Name=category_Name)

        # Create the product
        product = Product.objects.create(
            user=request.user,
            category=category,
            title=title,
            description=description,
            price=price,
            image=main_image,
            quantity=quantity
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



def providerDeleteProducts(request,id):
    pro=Product.objects.get(id=id)
    pro.delete()
    return redirect('provider:providerPanel')


def providerUpdateProducts(request, id):
    # Get the product instance using the product_id
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        # Process the form submission
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image') if 'image' in request.FILES else None

        # Update the product fields
        product.title = title
        product.description = description
        product.price = price

        if image:
            product.image = image

        product.save()
        
        return redirect('provider:providerPanel')  # Redirect to the provider panel or any other desired page

    return render(request, 'provider/providerUpdateProducts.html', {'product': product})



def providerApproval(request):
    ord = order.objects.filter(product__user=request.user)
    #total_price = ord.product.price * ord.quantity * ord.days_needed
    for i in ord:
        pprice=i.product.price
        q = i.quantity
        d = i.days_needed
        total_price = pprice*d*q
    context={
        'total_price':total_price,
        'ord':ord
    }
    return render(request, 'provider/providerApproval.html', context)
