from django.shortcuts import render, redirect
from products.models import Product, Category, Review
from products.forms import CreateProduct, CreateReview
from products.constants import PAGINATION_LIMIT


def main(request):
    return render(request, 'layouts/index.html')


def products_view(request):

    user = None if request.user.is_anonymous else request.user

    if request.method == 'GET':

        page = int(request.GET.get('page', 1))

        category_id = request.GET.get('category')

        search = request.GET.get('search')

        if category_id:
            products = Product.objects.filter(category__in=category_id)
        else:
            products = Product.objects.all()
        
        if search:
            products = Product.objects.filter(title__icontains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        if max_page > round(max_page):
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)
        
        products = products[PAGINATION_LIMIT*(page-1):PAGINATION_LIMIT*page]

        context = {
            'products': products,
            'user': user,
            'pages': range(1, max_page+1),
        }

        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):

    user = None if request.user.is_anonymous else request.user

    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'reviews': product.reviews.all(),
            'categorys': product.category.all(),
            'comment_form': CreateReview,
            'user': user,
            }
        return render(request, 'products/detail.html', context=context)
    
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        form = CreateReview(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                reviewer=request.user,
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
            'user': user,
            }
            return render(request, 'products/detail.html', context=context)


def all_categories_view(request):

    user = None if request.user.is_anonymous else request.user

    if request.method == 'GET':
        context = {
            'categorys': Category.objects.all(),
            'user': user,
        }
        return render(request, 'categories/categories.html', context=context)


def product_create_view(request):

    user = None if request.user.is_anonymous else request.user

    if request.method == 'GET':

        context = {
            'form': CreateProduct,
            'user': user,
            }

        return render(request, 'products/create.html',context=context)
    
    if request.method == 'POST':
        form = CreateProduct(data=request.POST)
        
        if form.is_valid():
            Product.objects.create(
                seller=request.user,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description')
            )

            return redirect('/products/')
        
        else:

            context = {
                'form': form,
                'user': user,
                }

            return render(request, 'products/create.html',context=context)