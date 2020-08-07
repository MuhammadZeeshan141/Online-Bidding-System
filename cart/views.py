from django.http import HttpResponse
from django.shortcuts import render, redirect

from account.views import validateEmail
from product.models import Product
from .models import Cart, Countries, Order
from django.db.models import Sum
from django.contrib import messages


# Create your views here.

def addToCart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        quantity = int(request.GET['quantity'])
        product = Product.objects.get(pk=product_id)
        if quantity > product.quantity or quantity <= 0 or quantity is None:
            return HttpResponse("Entered quantity is not valid")
        try:
            cart = Cart.objects.get(status=1, product=product, user=request.user)
        except Cart.DoesNotExist:
            cart = None
        if cart is None:
            cart = Cart()
            cart.price = product.price * quantity
            cart.quantity = quantity
            cart.status = 1
            cart.product = product
            cart.user = request.user
        else:
            cart.quantity = cart.quantity + quantity
            cart.price = cart.product.price * cart.quantity
        product.quantity = product.quantity - quantity
        product.save()
        cart.save()
        return HttpResponse("success")
    else:
        return HttpResponse("Request method is not a GET")


def cart(request):
    cart_items = Cart.objects.filter(status=1, user=request.user)
    total_products = cart_items.count
    total_price = list(cart_items.aggregate(Sum('price')).values())[0]
    context = {
        'total_products': total_products,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def remove_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST['cart_item_id']
        db_cart_item = Cart.objects.get(id=cart_item_id)
        product = db_cart_item.product
        product.quantity = product.quantity + db_cart_item.quantity
        product.save()
        db_cart_item.delete()

    return redirect('/cart')


def cart_item_increment(request):
    if request.method == 'POST':
        cart_item_increment = request.POST['cart_item_increment']
        db_cart_item = Cart.objects.get(id=cart_item_increment)
        product = db_cart_item.product
        if product.quantity > 0:
            db_cart_item.quantity = db_cart_item.quantity + 1
            product.quantity = product.quantity - 1
            product.save()
            db_cart_item.save()
        else:
            messages.error(request, 'No more items in stock', extra_tags='alert-danger')

    return redirect('/cart')


def cart_item_decrement(request):
    if request.method == 'POST':
        cart_item_decrement = request.POST['cart_item_decrement']
        db_cart_item = Cart.objects.get(id=cart_item_decrement)
        product = db_cart_item.product
        if db_cart_item.quantity > 1:
            db_cart_item.quantity = db_cart_item.quantity - 1
            product.quantity = product.quantity + 1
            product.save()
            db_cart_item.save()
        else:
            product.quantity = product.quantity + db_cart_item.quantity
            product.save()
            db_cart_item.delete()

    return redirect('/cart')


def checkout(request):
    countries_list = Countries.objects.all()
    cart_items = Cart.objects.filter(status=1, user=request.user)
    total_price = list(cart_items.aggregate(Sum('price')).values())[0]
    context = {
        'countries_list': countries_list,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    if request.method == 'POST':
        orders_list = []
        for item in cart_items:
            order = Order()
            order.firstName = request.POST['first_name']
            order.lastName = request.POST['last_name']
            order.phoneNumber = request.POST['number']
            order.email = request.POST['email']
            order.country = request.POST['country']
            order.adressLine1 = request.POST['add1']
            order.adressLine2 = request.POST['add2']
            order.city = request.POST['city']
            order.ZIP = request.POST['zip']
            order.user = request.user
            order.quantity = item.quantity
            order.product = item.product
            order.productPrice = item.price
            order.orderPrice = order.quantity * order.productPrice
            if order.firstName != '' and order.lastName != '' and order.phoneNumber != '' and order.email != '' and \
                    order.country != '' and order.adressLine1 != '' and order.city != '' and order.ZIP != '':
                if validateEmail(order.email):
                    order.save()
                    cart_items.delete()
                    orders_list.append(order)
                else:
                    (messages.error(request, 'Enter a valid Email', extra_tags='alert-danger'))
                    return render(request, 'checkout.html', context)
            else:
                messages.error(request, 'Please fill all the fields', extra_tags='alert-danger')
                return render(request, 'checkout.html', context)

            context = {
                'countries_list': countries_list,
                'cart_items': cart_items,
                'total_price': total_price,
                'orders': orders_list
            }
        return render(request, 'confirmation.html', context)

    return render(request, 'checkout.html', context)


def confirmation(request):
    return render(request, 'confirmation.html')
