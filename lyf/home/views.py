from django.shortcuts import render
from adminPanel.models import Product
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db.models import Q

@never_cache
def homePage(request):
    # Filter products where is_active is True and the users dont see there own products
    if request.user.is_authenticated:
        user = request.user
        proUser = Product.objects.filter(user=user)
        products = Product.objects.filter(is_active=True, rentable=True).exclude(id__in=proUser.values_list('id', flat=True))
        context = {'products': products}
        return render(request, 'homePage.html', context)
    else:
        products = Product.objects.filter(is_active=True, rentable=True)
        context = {'products': products}
        return render(request, 'homePage.html', context)


def searchbar(request):
    query = request.GET.get('q')
    context = {'products': [], 'query': query}
    user = request.user
    proUser = Product.objects.filter(user=user)
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(category__Name__icontains=query)
        ).exclude(id__in=proUser.values_list('id', flat=True))
        context['products'] = products

    return render(request, 'homePage.html', context)



def contactus(request):
    return render(request,'contactus.html')