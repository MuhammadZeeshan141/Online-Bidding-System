from django.shortcuts import render
from .models import Contact


# Create your views here.

def contact(request):
    if request.method == 'POST':
        cont = Contact()
        cont.name = request.POST['name']
        cont.email = request.POST['email']
        cont.subject = request.POST['subject']
        cont.message = request.POST['message']
        cont.save()

    return render(request, "contact.html")
