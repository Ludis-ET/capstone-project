from django.shortcuts import render

def index(request):
    return render(request, "pages/Home/home.html",{})


def shelf(request):
    return render(request, "pages/shelf/shelf.html",{})


def book(request,id):
    return render(request, "pages/shelf/BookDetail.html",{})
