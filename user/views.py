from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash

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
def add_borrow(request,username,id):
    previous_url = request.META.get('HTTP_REFERER')
    user = CustomUser.objects.get(username = username)
    if user == request.user:
        book = Book.objects.get(id=id)
        shelf, created = BorrowedBook.objects.get_or_create(user=user)
        shelf.book.add(book)
        if shelf.book.all().count() <= 3:
            if book.status != 'borrowed':
                book.status = 'borrowed'
                book.save()
                book.history.add(user)
                s = Shelf.objects.get(user=user)
                s.books.remove(book)
                s.save()
                shelf.save()
                messages.success(request, f"book {book.title} borrowed succesfully")
                return redirect(previous_url)
            messages.error(request, f"someone borrowed this book first")
            return redirect(previous_url)

        shelf.book.remove(book)
        messages.error(request, f"you can't borrow more then 3 books")
        return redirect(previous_url)

    messages.error(request, f"you can only borrow from your shelf")
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
def remove_book(request,username,id):
    previous_url = request.META.get('HTTP_REFERER')
    user = CustomUser.objects.get(username = username)
    if user == request.user:
        book = Book.objects.get(id=id)
        shelf, created = BorrowedBook.objects.get_or_create(user=user)
        shelf.book.remove(book)
        book.status = 'available'
        book.save()
        messages.success(request, f"book {book.title} was returned succesfully")
        return redirect(previous_url)
    messages.error(request, f"error")

@login_required
def profile(request,username):
    user = request.user
    favorite, created = Wishlist.objects.get_or_create(user=user)
    shelf, created = Shelf.objects.get_or_create(user=user)
    shelfs = BorrowedBook.objects.get(user=user)
    form = UserChangeForm(instance=user)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            if request.POST.get('change_password'):
                password = request.POST.get('new_password')
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your profile has been updated successfully and password changed.')
            else:
                messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    context = {
        'user': user,
        'fav':favorite,
        'shelf':shelf,
        'shelfs':shelfs
    }
    return render(request, "pages/user/profile.html",context)

@login_required
def wishlist(request,username):
    user = request.user
    favorite, created = Wishlist.objects.get_or_create(user=user)
    shelf, created = Shelf.objects.get_or_create(user=user)
    shelfs = Wishlist.objects.get(user=user)
    context = {
        'user': user,
        'fav':favorite,
        'shelf':shelf,
        'shelfs':shelfs
    }
    return render(request, "pages/user/wishlist.html",context)

@login_required
def shelf(request,username):
    user = request.user
    favorite, created = Wishlist.objects.get_or_create(user=user)
    shelf, created = Shelf.objects.get_or_create(user=user)
    shelfs = Shelf.objects.get(user=user)
    context = {
        'user': user,
        'fav':favorite,
        'shelf':shelf,
        'shelfs':shelfs
    }
    return render(request, "pages/user/shelf.html",context)