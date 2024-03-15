from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Book

def index(request):
    return render(request, "pages/Home/home.html", {})

def shelf(request):
    books = Book.objects.all()
    return render(request, "pages/shelf/shelf.html", {"books": books})

def book(request, id):
    return render(request, "pages/shelf/BookDetail.html", {})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'{form.cleaned_data.get("first_name")} account created successfully!')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
            return redirect('index')  # Redirect to index if registration fails
    else:
        messages.error(request, 'nothing to register')
    return redirect('index')  # Redirect to index if request method is not POST
