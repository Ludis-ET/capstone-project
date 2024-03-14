from django.shortcuts import render
from .models import *

def index(request):
    
    return render(request, "pages/Home/home.html",{})


def shelf(request):
    books = Book.objects.all()
    return render(request, "pages/shelf/shelf.html",{"books":books})


def book(request,id):
    return render(request, "pages/shelf/BookDetail.html",{})
