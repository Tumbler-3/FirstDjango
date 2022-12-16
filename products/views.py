from django.shortcuts import render
from products.models import Product


def main(request):
    return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'products/products.html', context={'products':products})
