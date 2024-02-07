import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import Categories, Product, coupons, ProductOffer, CategoryOffer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.models import CustomUser
from order.models import order
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.urls import reverse
from django.db.models import Q


def admin_access_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this page.")

    return wrapper
 

@admin_access_required
def adminAddProducts(request):
    pass


@admin_access_required
def adminCategory(request):
    cat = Categories.objects.all()
    return render(request, 'adminPanel/adminCategory.html', {'cat': cat})


@admin_access_required
def adminAddCategory(request):
    if request.method == 'POST':
        Name = request.POST.get('Name').strip()
        description = request.POST.get('Description')
        if not Name:
            messages.error(request, 'Category name is required')
        else:
            Categories.objects.create(Name=Name,description=description)
            messages.success(request, 'Category added successfully')
            return redirect('adminPanel:adminCategory')

    return render(request,'adminPanel/adminAddCategory.html')

@admin_access_required
def adminDeleteCategory(request,id):
    ct=Categories.objects.get(id=id)
    ct.delete()
    return redirect('adminPanel:adminCategory')

@admin_access_required
def adminUpdateCategory(request, id):
    cu = Categories.objects.get(id=id)

    if request.method == 'POST':
        Name = request.POST.get('Name').strip()
        description = request.POST.get('description')

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


@admin_access_required
def adminProducts(request):
    products=Product.objects.all()
    products_per_page = 10
    paginator = Paginator(products, products_per_page)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'adminPanel/adminProducts.html',{'products': products})


@admin_access_required
def renterList(request):
    renters = CustomUser.objects.all().exclude(is_staff=True)
    renters_per_page = 10
    paginator = Paginator(renters, renters_per_page)

    page = request.GET.get('page')
    try:
        renters = paginator.page(page)
    except PageNotAnInteger:
        renters = paginator.page(1)
    except EmptyPage:
        renters = paginator.page(paginator.num_pages)

    return render(request, 'adminPanel/renterList.html', {'renter': renters})

@admin_access_required
def providerList(request):
    provider=CustomUser.objects.filter(is_staff=True).exclude(is_superuser=True)
    provider_per_page = 10
    paginator = Paginator(provider, provider_per_page)

    page = request.GET.get('page')
    try:
        provider = paginator.page(page)
    except PageNotAnInteger:
        provider = paginator.page(1)
    except EmptyPage:
        provider = paginator.page(paginator.num_pages)
        
    return render(request,'adminPanel/providerList.html',{'provider':provider})

@admin_access_required
def blockUnblockUserProvider(request,id=id):
    if request.method == 'POST':
        u=CustomUser.objects.get(id=id)
        if u.is_active==True:
            u.is_active=False
        else:
            u.is_active=True
        u.save()
    return redirect('adminPanel:providerList')

@admin_access_required
def blockUnblockUserRenter(request,id=id):
    if request.method == 'POST':
        u=CustomUser.objects.get(id=id)
        if u.is_active==True:
            u.is_active=False
        else:
            u.is_active=True
        u.save()
    return redirect('adminPanel:renterList')

@admin_access_required
def activeDeactiveProducts(request,id=id):
    if request.method=='POST':
        ban=Product.objects.get(id=id)
        if ban.is_active==True:
            ban.is_active=False
        else:
            ban.is_active=True
        ban.save()
    return redirect('adminPanel:adminProducts')


@admin_access_required
def user_offers(request):
    return render(request,'adminPanel/adminPanel_offers.html')


@admin_access_required
def coupons_page(request):
    cop=coupons.objects.all()
    return render(request,'adminPanel/admin_coupons.html',{'cop':cop})

@admin_access_required
def add_coupons(request):
    COUPON_CHOICE = coupons.COUPON_CHOICE
    if request.method == 'POST':
        coupon_type=request.POST.get('coupon_type')
        name = request.POST.get('name').strip()
        discount = request.POST.get('discount')
        num = request.POST.get('num')
        if not name or not discount:
            messages.error(request, 'Please provide correct details')
        else:
            obj=coupons.objects.create(name=name,discount=discount,num=num,coupon_type=coupon_type)
            messages.success(request, 'Coupouns added successfully')
            return redirect('adminPanel:coupons_page')
    return render(request,'adminPanel/add_coupons.html',{'COUPON_CHOICE': COUPON_CHOICE })


@admin_access_required
def coupons_activate_deactivate(request,id):
    if request.method=='POST':
        cop=coupons.objects.get(id=id)
        if cop.is_active:
            cop.is_active=False
        else:
            cop.is_active=True
    cop.save()
    return redirect('adminPanel:coupons_page')



@admin_access_required
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



@admin_access_required
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
    
@admin_access_required
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


@admin_access_required
def pay_provider_success(request,id):
    ord=order.objects.get(id=id)
    ord.payment_provider=True
    ord.save()
    return redirect('order:rental_management')

@admin_access_required
def order_complete_details(request,id):
    ord=order.objects.get(id=id)
    return render(request,'adminPanel/order_complete_details.html',{'ord':ord})



def product_offer_form(request):
    product_offer = ProductOffer.objects.all()
    return render(request, 'adminPanel/adminPanel_offers.html', {'product_offer': product_offer})

def category_offer_form(request):
    categories_offer = CategoryOffer.objects.all()
    return render(request, 'adminPanel/adminPanel_offers_cat.html', {'categories_offer': categories_offer})


def add_product_offer(request):
    all_product=Product.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product')
        discount_percentage = request.POST.get('discount_percentage')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        today=datetime.now().date()
        if start_date < today:
            messages.error(request,'Please choose a valid date')
            return redirect('adminPanel:add_product_offer')
        if start_date > end_date:
            messages.error(request,'Please choose a valid date.')
            return redirect('adminPanel:add_product_offer')
        product = Product.objects.get(pk=product_id)
        ProductOffer.objects.create(product=product, discount_percentage=discount_percentage, start_date=start_date, end_date=end_date)
        return redirect('adminPanel:product_offer_form')
    return render(request,'adminPanel/add_product_offer.html',{'all_product':all_product})


def add_category_offer(request):
    categories=Categories.objects.all()
    print(categories)
    if request.method == 'POST':
        category_id = request.POST.get('category')
        discount_percentage = request.POST.get('discount_percentage')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        today=datetime.now().date()
        if start_date < today:
            messages.error(request,'Please choose a valid date')
            return redirect('adminPanel:add_category_offer')
        if start_date > end_date:
            messages.error(request,'Please choose a valid date.')
            return redirect('adminPanel:add_category_offer')
        category = Categories.objects.get(pk=category_id)
        CategoryOffer.objects.create(category=category, discount_percentage=discount_percentage, start_date=start_date, end_date=end_date)
        return redirect('adminPanel:category_offer_form')
    return render(request,'adminPanel/add_category_offer.html',{'categories':categories})


def block_unblock_pro(request,id):
    pro_offer=ProductOffer.objects.get(id=id)
    if pro_offer.is_active:
        pro_offer.is_active=False
    else:
        pro_offer.is_active=True
    pro_offer.save()
    return redirect('adminPanel:product_offer_form')

def block_unblock_cat(request,id):
    cat_offer=CategoryOffer.objects.get(id=id)
    if cat_offer.is_active:
        print('ee')
        cat_offer.is_active=False
    else:
        cat_offer.is_active=True
    cat_offer.save()
    print('he')
    return redirect('adminPanel:category_offer_form')


def product_searchbar(request):
    query = request.GET.get('q')
    context = {'products': [], 'query': query}
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(category__Name__icontains=query)
        )
        context['products'] = products

    return render(request, 'adminPanel/adminProducts.html', context)


def rental_searchbar(request):
    query = request.GET.get('q')
    context = {'ord': [], 'query': query}
    if query:
        ord = order.objects.filter(
            Q(product__title__icontains=query) | Q(user__first_name__icontains=query)
            |Q(user__last_name__icontains=query)
            
        )
        context['ord'] = ord

    return render(request, 'adminPanel/adminRentalDetails.html', context)



def provider_searchbar(request):
    query = request.GET.get('q')
    context = {'provider': [], 'query': query}
    if query:
        provider = CustomUser.objects.filter(
            Q(first_name__icontains=query) 
            |Q(last_name__icontains=query)
            
        )
        context['provider'] = provider

    return render(request, 'adminPanel/providerList.html', context)


def renter_searchbar(request):
    query = request.GET.get('q')
    context = {'renter': [], 'query': query}
    if query:
        renter = CustomUser.objects.filter(
            Q(first_name__icontains=query) 
            |Q(last_name__icontains=query)
            
        )
        context['renter'] = renter

    return render(request, 'adminPanel/renterList.html', context)