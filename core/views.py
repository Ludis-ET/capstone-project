from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib import messages

def index(request):
    return render(request, "pages/Home/home.html",{})

def register(request):
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'{form.first_name} account created successfuly!')
            return redirect(previous_url)
        else:
            messages.error(request, form.errors)
            return redirect(previous_url)
    else:
        return HttpResponse("<h1 style='position:absolute;top:30%;left:40%;'>Nothing to register</h1>")


def shelf(request):
    # books = Book.objects.all()
    return render(request, "pages/shelf/shelf.html",{})


def book(request,id):
    return render(request, "pages/shelf/BookDetail.html",{})
