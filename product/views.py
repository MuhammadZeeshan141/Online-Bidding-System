from django.shortcuts import render
from product.models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def home(request):
    products = Product.objects.all()
    featured_product = Product.objects.get(pk=5)
    context = {
        'products': products,
        'featured_product': featured_product
    }
    return render(request, 'home.html', context)


def product_index(request):
    products_list = Product.objects.all()
    total_products = products_list.count
    paginator = Paginator(products_list, 1)
    page = request.GET.get('page', 1)
    categories = Category.objects.all()
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'total_products': total_products,
        'products': products,
        'categories': categories,
        'paginator': paginator
    }
    return render(request, 'product_index.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)


def products_by_category(request, pk):
    category = Category.objects.get(pk=pk)
    products_list = category.products.all()
    total_products = products_list.count
    paginator = Paginator(products_list, 1)
    page = request.GET.get('page', 1)
    categories = Category.objects.all()
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'total_products': total_products,
        'category': category,
        'products': products,
        'categories': categories,
        'paginator': paginator
    }
    return render(request, 'products_by_category.html', context)
