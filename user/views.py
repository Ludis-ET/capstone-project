from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Book
from .models import *

@login_required
def add_wishlist(request,username,id):
    previous_url = request.META.get('HTTP_REFERER')
    user = CustomUser.objects.get(username = username)
    if user == request.user:
        book = Book.objects.get(id=id)
        shelf, created = Wishlist.objects.get_or_create(user=user)
        shelf.books.add(book)
        messages.success(request, f"book {book.title} was added to your favorite list")
        return redirect(previous_url)
    messages.error(request, f"you can only add to your favorites list")
    return redirect(previous_url)

@login_required
def remove_wishlist(request,username,id):
    previous_url = request.META.get('HTTP_REFERER')
    user = CustomUser.objects.get(username = username)
    if user == request.user:
        book = Book.objects.get(id=id)
        shelf, created = Wishlist.objects.get_or_create(user=user)
        shelf.books.remove(book)
        messages.success(request, f"book {book.title} was removed from your favorite list")
        return redirect(previous_url)
    messages.error(request, f"you can only remove from your favorites list")


@login_required
def add_shelf(request,username,id):
    previous_url = request.META.get('HTTP_REFERER')
    user = CustomUser.objects.get(username = username)
    if user == request.user:
        book = Book.objects.get(id=id)
        shelf, created = Shelf.objects.get_or_create(user=user)
        shelf.books.add(book)
        messages.success(request, f"book {book.title} was added to shelf")
        return redirect(previous_url)
    messages.error(request, f"you can only add to your shelf")
    return redirect(previous_url)

@login_required
def remove_shelf(request,username,id):
    previous_url = request.META.get('HTTP_REFERER')
    user = CustomUser.objects.get(username = username)
    if user == request.user:
        book = Book.objects.get(id=id)
        shelf, created = Shelf.objects.get_or_create(user=user)
        shelf.books.remove(book)
        messages.success(request, f"book {book.title} was removed from your shelf")
        return redirect(previous_url)
    messages.error(request, f"you can only remove from your shelf")

@login_required
def profile(request,username):
    return render(request, "pages/user/profile.html",{"username":username})

@login_required
def wishlist(request,username):
    return render(request, "pages/user/wishlist.html",{"username":username})

@login_required
def shelf(request,username):
    return render(request, "pages/user/shelf.html",{"username":username})