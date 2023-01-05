from django.shortcuts import render, redirect
from products.models import Product, Category, Review
from products.forms import CreateProduct, CreateReview
from products.constants import PAGINATION_LIMIT
from django.views.generic import ListView


def main(request):
    return render(request, 'layouts/index.html')


class ProductsView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'products': kwargs['products'],
            'user': kwargs['user'],
            'pages': kwargs['pages']
        }
        return context

    def get(self, request, **kwargs):
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

        return render(request, self.template_name, context=self.get_context_data(
            products=products,
            user=None if request.user.is_anonymous else request.user,
            pages=range(1, max_page+1),
        ))


class ProductDetailView(ListView):
    template_name = 'products/detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = {
            'product': kwargs['product'],
            'reviews': kwargs['reviews'],
            'categorys': kwargs['categorys'],
            'comment_form': kwargs['comment_form'],
            'user': kwargs['user'],
        }
        return context

    def get(self, request, id, **kwargs,):
        product = self.model.objects.get(id=id)
        return render(request, self.template_name, context=self.get_context_data(
            product=product,
            reviews=product.reviews.all(),
            categorys=product.category.all(),
            comment_form=CreateReview,
            user=None if request.user.is_anonymous else request.user
        ))

    def post(self, request, id, **kwargs):
        product = self.model.objects.get(id=id)
        form = CreateReview(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                reviewer=request.user,
                product=product,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{id}/')

        else:
            return render(request, self.template_name, context=self.get_context_data(
                product=product,
                reviews=product.reviews.all(),
                categorys=product.category.all(),
                comment_form=form,
                user=None if request.user.is_anonymous else request.user
            ))


class AllCategoriesView(ListView):
    template_name = 'categories/categories.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = {
            'categorys': kwargs['categorys'],
            'user': kwargs['user'],
        }
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data(
            categorys=self.model.objects.all(),
            user=None if request.user.is_anonymous else request.user
        ))


class ProductCreateView(ListView):
    template_name='products/create.html'
    
    def get_context_data(self, **kwargs):
        context = {
            'form': kwargs['form'],
            'user': kwargs['user'],
        }
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data(
            form=CreateProduct,
            user=None if request.user.is_anonymous else request.user
        ))

    def post(self, request, **kwargs):
        form = CreateProduct(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                seller=request.user,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description')
            )

            return redirect('/products/')

        else:
            return render(request, self.template_name, context=self.get_context_data(
                form=form,
                user=None if request.user.is_anonymous else request.user
            ))