from django.shortcuts import render, redirect
from .models import Categories, Product, coupons
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.models import CustomUser
from order.models import order

@login_required(login_url='user:perform_login')
def adminPanel(request):
    return render(request, 'adminPanel/adminPanel.html')


@login_required(login_url='user:perform_login')
def adminProducts(request):
    products=Product.objects.all()
    return render(request, 'adminPanel/adminProducts.html',{'products': products})


@login_required(login_url='user:perform_login')
def adminAddProducts(request):
    pass


@login_required(login_url='user:perform_login')
def adminCategory(request):
    cat = Categories.objects.all()
    return render(request, 'adminPanel/adminCategory.html', {'cat': cat})


@login_required(login_url='user:perform_login')
def adminAddCategory(request):
    if request.method == 'POST':
        Name = request.POST.get('Name')
        description = request.POST.get('Description')
        Products = request.POST.get('Products')

        if not Name:
            messages.error(request, 'Category name is required')
        else:
            # Add logic to save the category or perform other actions on valid data
            # For example: Categories.objects.create(Name=Name, description=description, Products=Products)
            obj=Categories.objects.create(Name=Name,description=description)
            messages.success(request, 'Category added successfully')
            return redirect('adminPanel:adminCategory')

    # Redirect to the adminCategory view in both success and failure cases
    return render(request,'adminPanel/adminAddCategory.html')


def adminDeleteCategory(request,id):
    ct=Categories.objects.get(id=id)
    ct.delete()
    return redirect('adminPanel:adminCategory')


def adminUpdateCategory(request, id):
    # Get the category instance using the id
    cu = Categories.objects.get(id=id)

    if request.method == 'POST':
        # Process the form submission
        Name = request.POST.get('Name')
        description = request.POST.get('description')

        # Update category fields if provided
        if Name:
            cu.Name = Name
        if description:
            cu.description = description

        if not Name:
            messages.error(request, 'Invalid data')
        else:
            cu.save()
            return redirect('adminPanel:adminCategory')
    
    return render(request, 'adminPanel/adminUpdateCategory.html', {'cu': cu})



def renterList(request):
    renter=CustomUser.objects.all().exclude(is_staff=True)
    return render(request,'adminPanel/renterList.html',{'renter':renter})

def providerList(request):
    provider=CustomUser.objects.filter(is_staff=True).exclude(is_superuser=True)
    return render(request,'adminPanel/providerList.html',{'provider':provider})

def blockUnblockUserProvider(request,id=id):
    if request.method == 'POST':
        u=CustomUser.objects.get(id=id)
        if u.is_active==True:
            u.is_active=False
        else:
            u.is_active=True
        u.save()
    return redirect('adminPanel:providerList')


def blockUnblockUserRenter(request,id=id):
    if request.method == 'POST':
        u=CustomUser.objects.get(id=id)
        if u.is_active==True:
            u.is_active=False
        else:
            u.is_active=True
        u.save()
    return redirect('adminPanel:renterList')


def activeDeactiveProducts(request,id=id):
    if request.method=='POST':
        ban=Product.objects.get(id=id)
        if ban.is_active==True:
            ban.is_active=False
        else:
            ban.is_active=True
        ban.save()
    return redirect('adminPanel:adminProducts')


def coupons_page(request):
    cop=coupons.objects.all()
    return render(request,'adminPanel/admin_coupons.html',{'cop':cop})

def add_coupons(request):
    COUPON_CHOICE = coupons.COUPON_CHOICE
    if request.method == 'POST':
        coupon_type=request.POST.get('coupon_type')
        name = request.POST.get('name')
        discount = request.POST.get('discount')
        num = request.POST.get('num')
        if not name:
            messages.error(request, 'Name is required')
        
        else:
            obj=coupons.objects.create(name=name,discount=discount,num=num,coupon_type=coupon_type)
            messages.success(request, 'Coupouns added successfully')
            return redirect('adminPanel:coupons_page')

    return render(request,'adminPanel/add_coupons.html',{'COUPON_CHOICE': COUPON_CHOICE })


def coupons_activate_deactivate(request,id):
    if request.method=='POST':
        cop=coupons.objects.get(id=id)
        if cop.is_active:
            cop.is_active=False
        else:
            cop.is_active=True
    cop.save()
    return redirect('adminPanel:coupons_page')