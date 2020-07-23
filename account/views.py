from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect


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

        if username != '' and password1 != '' and password2 != '' and email != '' and first_name != '' and last_name != '':
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
                        user.save()
                        messages.success(request, 'User created', extra_tags='alert-success')
                        return redirect('login')
                else:
                    messages.error(request, 'Password does not match', extra_tags='alert-danger')
                    return redirect('signup')
            else:
                (messages.error(request, 'Enter a valid Email', extra_tags='alert-danger'))
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