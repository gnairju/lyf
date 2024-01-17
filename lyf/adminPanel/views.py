import csv
from django.shortcuts import render, redirect
from .models import Categories, Product, coupons, offers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.models import CustomUser
from order.models import order
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


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
            obj=Categories.objects.create(Name=Name,description=description)
            messages.success(request, 'Category added successfully')
            return redirect('adminPanel:adminCategory')

    return render(request,'adminPanel/adminAddCategory.html')


def adminDeleteCategory(request,id):
    ct=Categories.objects.get(id=id)
    ct.delete()
    return redirect('adminPanel:adminCategory')


def adminUpdateCategory(request, id):
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



def user_offers(request):
    return render(request,'adminPanel/adminPanel_offers.html')


def add_user_offer(request):
    if request.method == 'POST':
        name=request.POST.get('offer_name')
        offer_type=request.POST.get('offer_type')
        offer_percentage=request.POST.get('offer_percentage')
        offers.objects.create(
            name=name,
            offer_type=offer_type,
            offer_percentage=offer_percentage
        )
        messages.success(request, 'Coupouns added successfully')
        return redirect('adminPanel:add_user_offer')
    return render(request,'adminPanel/add_user_offer.html',{})


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



@login_required(login_url='user:perform_login')
def adminPanel(request, chart_labels=None, chart_data=None, chart_labels_month=None, chart_data_month=None):
    orders = order.objects.all()

    orders_by_month = {}
    orders_by_year = {}
    orders_by_day = {}

    for o in orders:
        month = o.date.month
        if month in orders_by_month:
            orders_by_month[month] += o.quantity
        else:
            orders_by_month[month] = o.quantity

        year = o.date.year
        if year in orders_by_year:
            orders_by_year[year] += o.quantity
        else:
            orders_by_year[year] = o.quantity

        day = o.date.day
        if day in orders_by_day:
            orders_by_day[day] += o.quantity
        else:
            orders_by_day[day] = o.quantity

    detailed_report = None

    if request.method == 'POST':
        report = request.POST.get('status')

        if report == 'yearly':
            chart_labels = list(orders_by_year.keys())
            chart_data = list(orders_by_year.values())
            detailed_report = order.objects.filter(date__year=datetime.now().year)

        elif report == 'monthly':
            chart_labels = list(orders_by_month.keys())
            chart_data = list(orders_by_month.values())
            detailed_report = order.objects.filter(date__month=datetime.now().month)

        elif report == 'daily':
            chart_labels = list(orders_by_day.keys())
            chart_data = list(orders_by_day.values())
            detailed_report = order.objects.filter(date=datetime.now().date())

    return render(request, 'adminPanel/adminPanel.html', {'chart_labels': chart_labels, 'chart_data': chart_data, 'detailed_report': detailed_report})


def download_detailed_report(request):
    if request.method=='POST':
        status = request.POST.get('status')
        print('status',status)
        orders = None
        if status == 'yearly':
            orders = order.objects.filter(date__year=datetime.now().year)
        elif status == 'monthly':
            orders = order.objects.filter(date__month=datetime.now().month)
        elif status == 'daily':
            orders = order.objects.filter(date=datetime.now().date())

        
        
        request.session['status']=status

        if orders:
            return render(request, 'adminPanel/adminPanel_report.html', {'orders': orders})
        else:
            return render(request, 'adminPanel/adminPanel_report.html')
    
def report_download(request):
    template = get_template('adminPanel/adminPanel_report.html')
    status=request.session['status']
    if status == 'yearly':
        orders = order.objects.filter(date__year=datetime.now().year)
    elif status == 'monthly':
        orders = order.objects.filter(date__month=datetime.now().month)
    elif status == 'daily':
        orders = order.objects.filter(date=datetime.now().date())
    context={
            'orders':orders,
        }
    
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="your_pdf_filename.pdf"'

    # Create a PDF object
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If there are any error messages, show them
    if pisa_status.err:
        return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisa_status.err, html))

    return response



def pay_provider_success(request,id):
    ord=order.objects.get(id=id)
    ord.payment_provider=True
    ord.save()
    return redirect('order:rental_management')


