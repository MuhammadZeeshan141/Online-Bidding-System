from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth


# Create your views here.

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirmPassword']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.INFO(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.INFO(request, 'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1)
                user.save();
                print('User created')
                return redirect('login')
        else:
            print('Password does not match')
            return redirect('signup')

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
            # messages.INFO(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')
