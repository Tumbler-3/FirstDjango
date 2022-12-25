from django.shortcuts import render, redirect
from products.models import Product, Category, Review
from products.forms import CreateProduct, CreateReview


def main(request):
    return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':

        category_id = request.GET.get('category')

        if category_id:
            products = Product.objects.filter(category__in=category_id)
        else:
            products = Product.objects.all()

        context = {
            'products': products
        }

        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'reviews': product.reviews.all(),
            'categorys': product.category.all(),
            'comment_form': CreateReview,
            }
        return render(request, 'products/detail.html', context=context)
    
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        form = CreateReview(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                product=product,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{id}/')

        else:
            context = {
            'product': product,
            'reviews': product.reviews.all(),
            'categorys': product.category.all(),
            'comment_form': form,
            }
            return render(request, 'products/detail.html', context=context)


def all_categories_view(request):
    if request.method == 'GET':
        context = {
            'categorys': Category.objects.all()
        }
        return render(request, 'categories/categories.html', context=context)


def product_create_view(request):
    if request.method == 'GET':

        context = {'form': CreateProduct}

        return render(request, 'products/create.html',context=context)
    
    if request.method == 'POST':
        form = CreateProduct(data=request.POST)
        
        if form.is_valid():
            Product.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description')
            )

            return redirect('/products/')
        
        else:

            context = {'form': form}

            return render(request, 'products/create.html',context=context)