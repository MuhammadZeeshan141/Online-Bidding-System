from django.shortcuts import render

from account.views import validateEmail
from .models import Contact
from django.contrib import messages


# Create your views here.

def contact(request):
    if request.method == 'POST':
        cont = Contact()
        cont.name = request.POST['name']
        cont.email = request.POST['email']
        cont.subject = request.POST['subject']
        cont.message = request.POST['message']
        if cont.name != '' and cont.email != '' and cont.subject != '' and cont.message != '':
            if validateEmail(cont.email):
                cont.save()
                messages.success(request, 'Message sent successfully', extra_tags='alert-success')
            else:
                (messages.error(request, 'Enter a valid Email', extra_tags='alert-danger'))
        else:
            messages.error(request, 'Please fill all the fields', extra_tags='alert-danger')

    return render(request, "contact.html")
