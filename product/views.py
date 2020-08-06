from django.shortcuts import render
from product.models import Product, Category, History
from bidding.models import BidHistory, Records
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


# Create your views here.

def home(request):
    products = Product.objects.filter(type='purchase').order_by('-id')[:4:1]
    dateTimeNow = datetime.now()
    bidding_products = Records.objects.filter(startDateTime__lte=dateTimeNow, endDateTime__gte=dateTimeNow).order_by(
        '-id')[:4:1]
    context = {
        'products': products,
        'bidding_products': bidding_products,
    }
    if request.user.is_authenticated:
        categories_list = History.objects.filter(customer=request.user).values_list('category_id', flat=True).order_by(
            '-id')[:1:1]
        recommendations_list = Product.objects.exclude(type='bid').filter(category_id__in=categories_list)[:4:1]
        context['recommendations_list'] = recommendations_list

    return render(request, 'home.html', context)


def product_index(request):
    products_list = Product.objects.filter(type='purchase') | Product.objects.filter(type='both')
    total_products = products_list.count
    paginator = Paginator(products_list, 9)
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


def product_ascending(request):
    products_list = Product.objects.filter(type='purchase').order_by('price') | Product.objects.filter(
        type='both').order_by('price')
    total_products = products_list.count
    paginator = Paginator(products_list, 9)
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


def product_descending(request):
    products_list = Product.objects.filter(type='purchase').order_by('-price') | Product.objects.filter(
        type='both').order_by('-price')
    total_products = products_list.count
    paginator = Paginator(products_list, 9)
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
    if request.user.is_authenticated:
        history = History.objects.filter(product=pk, customer=request.user)
        if history is not None:
            history.delete()
        new_history = History()
        new_history.product = product
        new_history.customer = request.user
        new_history.category = product.category
        new_history.save()
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)


def products_by_category(request, pk):
    category = Category.objects.get(pk=pk)
    products_list = category.products.filter(type='purchase') | category.products.filter(type='both')
    total_products = products_list.count
    paginator = Paginator(products_list, 9)
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


def recommendations(request):
    categories_list = History.objects.filter(customer=request.user).values_list('category_id', flat=True).order_by(
        '-id')
    unique_list = []
    for x in categories_list:
        if len(unique_list) < 5:
            if x not in unique_list:
                unique_list.append(x)
    products_list = Product.objects.exclude(type='bid').filter(category_id__in=unique_list)
    total_products = products_list.count
    paginator = Paginator(products_list, 9)
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
        'paginator': paginator,
        'type': 'shop',
        'breadcrumb': 'Shop'
    }
    return render(request, 'recommendation.html', context)


def bidding_recommendations(request):
    categories_list = BidHistory.objects.filter(customer=request.user).values_list('category_id', flat=True).order_by(
        '-id')
    unique_list = []
    for x in categories_list:
        if len(unique_list) < 5:
            if x not in unique_list:
                unique_list.append(x)
    dateTimeNow = datetime.now()
    products_list = Records.objects.filter(product__category_id__in=unique_list, startDateTime__lte=dateTimeNow,
                                           endDateTime__gte=dateTimeNow)
    total_products = products_list.count
    paginator = Paginator(products_list, 9)
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
        'paginator': paginator,
        'type': 'bid',
        'breadcrumb': 'Bidding'
    }
    return render(request, 'recommendation.html', context)


def search(request):
    search = request.POST['search_input']
    products_list = Product.objects.filter(title__icontains=search, type='purchase') | Product.objects.filter(
        title__icontains=search, type='both')
    total_products = products_list.count
    paginator = Paginator(products_list, 9)
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
    return render(request, 'search.html', context)
