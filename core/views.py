from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def index(request):
    return render(request, "pages/Home/home.html",{})

def register(request):
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'{form.cleaned_data.get("first_name")} account created successfully!')
            return redirect(previous_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f' {error}')
            return redirect(previous_url)
    messages.error(request, 'nothing to register')
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect('index')
        

def login(request):
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'{user.first_name} logged in successfully!')
        else:
            messages.error(request, f'Invalid username and password combination')
        return redirect(previous_url)
    messages.error(request, "can't do authentication with nothing")
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect('index')


def shelf(request):
    # books = Book.objects.all()
    return render(request, "pages/shelf/shelf.html",{})


def book(request,id):
    return render(request, "pages/shelf/BookDetail.html",{})
