from django.shortcuts import render
from adminPanel.models import Product
from django.views.decorators.cache import never_cache

@never_cache
def homePage(request):
    # Filter products where is_active is True
    products = Product.objects.filter(is_active=True)
    print(products)
    context = {'products': products}
    return render(request, 'homePage.html', context)
