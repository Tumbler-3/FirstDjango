from django.shortcuts import render
from products.models import Product


def main(request):
    return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'products/products.html', context={'products':products})


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        return render(request, 'products/detail.html', context={'product':product, 'reviews':product.reviews.all()})