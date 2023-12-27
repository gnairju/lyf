from django.shortcuts import render
from adminPanel.models import Product
from django.views.decorators.cache import never_cache

@never_cache
def homePage(request):
    # Filter products where is_active is True and the users dont see there own products
    if request.user.is_authenticated:
        user = request.user
        proUser = Product.objects.filter(user=user)
        products = Product.objects.filter(is_active=True).exclude(id__in=proUser.values_list('id', flat=True))
        context = {'products': products}
        return render(request, 'homePage.html', context)
    else:
        products = Product.objects.filter(is_active=True)
        context = {'products': products}
        return render(request, 'homePage.html', context)
