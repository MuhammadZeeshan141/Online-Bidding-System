from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect

from bidding.models import Transactions
from cart.models import Order, OrderMessage


# Create your views here.
def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirmPassword']
        user_role = request.POST['userrole']

        if username != '' and password1 != '' and password2 != '' and email != '' and first_name != '' and last_name != '' and user_role != '':
            if validateEmail(email):
                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Username Taken', extra_tags='alert-danger')
                        return redirect('signup')
                    elif User.objects.filter(email=email).exists():
                        messages.error(request, 'Email Taken', extra_tags='alert-danger')
                        return redirect('signup')
                    else:
                        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                        email=email, password=password1)
                        if user_role == 'vendor':
                            user.is_staff = True
                            user.save()
                            user1 = User.objects.get(username=username)
                            group = Group.objects.get(pk=1)
                            user1.groups.add(group)
                        else:
                            user.save()
                        messages.success(request, 'User created', extra_tags='alert-success')
                        return redirect('login')
                else:
                    messages.error(request, 'Password does not match', extra_tags='alert-danger')
                    return redirect('signup')
            else:
                messages.error(request, 'Enter a valid Email', extra_tags='alert-danger')
        else:
            messages.error(request, 'Please fill all the fields', extra_tags='alert-danger')

    return render(request, "signup.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials', extra_tags='alert-danger')
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def accountDetails(request):
    user = request.user
    order_items = Order.objects.filter(status='pending', user=user)
    bid_items = Transactions.objects.filter(user=user)
    context = {
        'user': user,
        'order_items': order_items,
        'bid_items': bid_items
    }
    return render(request, "user_profile.html", context)


def contactVendor(request, pk):
    all_messages = OrderMessage.objects.filter(order=pk).order_by('-id')
    context = {
        'order_id': pk,
        'all_messages': all_messages
    }
    return render(request, "order_messages.html", context)


def sendMessage(request):
    order = Order.objects.get(pk=request.POST['order_id'])
    all_messages = OrderMessage.objects.filter(order=order.id)
    if request.method == 'POST':
        order_messages = OrderMessage()
        order_messages.order = order
        order_messages.customer = request.user
        order_messages.vendor = order.product.created_by
        order_messages.message = request.POST['message']
        order_messages.msg_from = 'customer'
        if order_messages.message != '':
            order_messages.save()
            messages.success(request, 'Message sent', extra_tags='alert-success')
        else:
            messages.error(request, 'Message not sent: Write a message', extra_tags='alert-danger')
    order_id = str(order.id);
    return redirect('/ContactVendor/' + order_id)
