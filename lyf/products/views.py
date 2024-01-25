from django.shortcuts import render, get_object_or_404
from adminPanel.models import Product

def productPage(request, id):
    product = get_object_or_404(Product, id=id)
    context={
        'product':product,
    }
    return render(request, 'products/productPage.html', context)
 