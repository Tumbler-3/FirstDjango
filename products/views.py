from django.shortcuts import render
from products.models import Product, Category


def main(request):
    return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':

        category_id = request.GET.get('category')

        if category_id:
            products = Product.objects.filter(category__in = category_id)
        else:
            products = Product.objects.all()

        context = {
            'products':products
        }
        
        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product':product, 
            'reviews':product.reviews.all(),
            'categorys': product.category.all()}
        return render(request, 'products/detail.html', context=context)


def all_categories_view(request):
    if request.method == 'GET':
        context = {
            'categorys': Category.objects.all()
        }
        return render(request, 'categories/categories.html', context=context)