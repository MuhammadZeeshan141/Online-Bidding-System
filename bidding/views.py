from django.http import HttpResponse
from django.shortcuts import render
from .models import Records, Transactions, BidHistory
from product.models import Product, Category
from cart.models import Countries
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timezone
from django.contrib import messages


# Create your views here.

def placeYourBid(request):
    if request.method == 'GET':
        record_id = request.GET['record_id']
        product_id = request.GET['product_id']
        record = Records.objects.get(pk=record_id)
        product = Product.objects.get(pk=product_id)
        bidding_amount = request.GET['bidding']
        if int(bidding_amount) < record.minimumBid:
            return HttpResponse("Entered amount is less than minimum bidding amount")
        try:
            transaction = Transactions.objects.get(record=record, user=request.user, status='pending')
        except Transactions.DoesNotExist:
            transaction = None
        if transaction is None:
            transaction = Transactions()
            transaction.product = product
            transaction.record = record
            transaction.user = request.user
            transaction.biddingAmount = bidding_amount
            transaction.phoneNumber = request.GET['phone_number']
            transaction.country = request.GET['country']
            transaction.city = request.GET['city']
            transaction.adressLine1 = request.GET['address1']
            transaction.adressLine2 = request.GET['address2']
            transaction.ZIP = request.GET['zip']
            if transaction.phoneNumber == '' or transaction.country == '' or transaction.city == '' or transaction.adressLine1 == '' or transaction.ZIP == '':
                return HttpResponse("Incomplete form: Please Fill all the fields")
        else:
            transaction.biddingAmount = bidding_amount
        transaction.save()
        return HttpResponse("success")
    else:
        return HttpResponse("Request method is not a GET")


def bidding_index(request):
    dateTimeNow = datetime.now()
    products_list = Records.objects.filter(startDateTime__lte=dateTimeNow, endDateTime__gte=dateTimeNow)
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
        'type': "active",
        'breadcrumb': "Active",
        'total_products': total_products,
        'products': products,
        'categories': categories,
        'paginator': paginator
    }
    return render(request, "bidding_index.html", context)


def coming_soon_bidding_index(request):
    dateTimeNow = datetime.now()
    products_list = Records.objects.filter(startDateTime__gte=dateTimeNow, endDateTime__gte=dateTimeNow)
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
        'type': "coming_soon",
        'breadcrumb': "Coming Soon",
        'total_products': total_products,
        'products': products,
        'categories': categories,
        'paginator': paginator
    }
    return render(request, "bidding_index.html", context)


def bidding_ascending(request, type):
    dateTimeNow = datetime.now()
    if type == 'coming_soon':
        records_list = Records.objects.filter(startDateTime__gte=dateTimeNow, endDateTime__gte=dateTimeNow).order_by(
            'minimumBid')
        breadcrumb = "Coming Soon"
    else:
        records_list = Records.objects.filter(startDateTime__lte=dateTimeNow, endDateTime__gte=dateTimeNow).order_by(
            'minimumBid')
        breadcrumb = "Active"
    total_products = records_list.count
    paginator = Paginator(records_list, 9)
    page = request.GET.get('page', 1)
    categories = Category.objects.all()
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'type': type,
        'total_products': total_products,
        'products': products,
        'categories': categories,
        'paginator': paginator,
        'breadcrumb': breadcrumb
    }
    return render(request, 'bidding_index.html', context)


def bidding_descending(request, type):
    dateTimeNow = datetime.now()
    if type == 'coming_soon':
        records_list = Records.objects.filter(startDateTime__gte=dateTimeNow, endDateTime__gte=dateTimeNow).order_by(
            '-minimumBid')
        breadcrumb = "Coming Soon"
    else:
        records_list = Records.objects.filter(startDateTime__lte=dateTimeNow, endDateTime__gte=dateTimeNow).order_by(
            '-minimumBid')
        breadcrumb = "Active"
    total_products = records_list.count
    paginator = Paginator(records_list, 9)
    page = request.GET.get('page', 1)
    categories = Category.objects.all()
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'type': type,
        'total_products': total_products,
        'products': products,
        'categories': categories,
        'paginator': paginator,
        'breadcrumb': breadcrumb
    }
    return render(request, 'bidding_index.html', context)


def bidding_detail(request, pk, type):
    countries_list = Countries.objects.all()
    bidding = Records.objects.get(pk=pk)
    difference = 0
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    dateTimeNow = datetime.now(timezone.utc)
    if type == 'coming_soon':
        difference = bidding.startDateTime - dateTimeNow
    else:
        difference = bidding.endDateTime - dateTimeNow
    time = abs(int(difference.total_seconds()))
    days = time // (24 * 3600)
    time = time % (24 * 3600)
    hours = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    if request.user.is_authenticated:
        history = BidHistory.objects.filter(record=pk, customer=request.user)
        if history is not None:
            history.delete()
        new_history = BidHistory()
        new_history.record = bidding
        new_history.customer = request.user
        new_history.category = bidding.product.category
        new_history.save()
    context = {
        'countries_list': countries_list,
        'bidding': bidding,
        'type': type,
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'difference': time
    }
    return render(request, 'bidding_detail.html', context)


def bidding_by_category(request, pk, type):
    dateTimeNow = datetime.now()
    if type == 'coming_soon':
        records_list = Records.objects.filter(startDateTime__gte=dateTimeNow, endDateTime__gte=dateTimeNow,
                                              product__category__pk=pk)
        breadcrumb = "Coming Soon"
    else:
        records_list = Records.objects.filter(startDateTime__lte=dateTimeNow, endDateTime__gte=dateTimeNow,
                                              product__category__pk=pk)
        breadcrumb = "Active"
    category = Category.objects.get(pk=pk)
    # products_list = category.products.filter(type='bid') | category.products.filter(type='both')
    total_products = records_list.count
    paginator = Paginator(records_list, 9)
    page = request.GET.get('page', 1)
    categories = Category.objects.all()
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'type': type,
        'total_products': total_products,
        'category': category,
        'products': products,
        'categories': categories,
        'paginator': paginator,
        'breadcrumb': breadcrumb
    }
    return render(request, 'bidding_by_category.html', context)
