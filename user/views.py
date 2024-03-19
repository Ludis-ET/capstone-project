from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


from core.models import Book
from .models import *

@login_required(login_url='index')
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

@login_required(login_url='index')
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


@login_required(login_url='index')
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

@login_required(login_url='index')
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

@login_required(login_url='index')
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


@login_required(login_url='index')
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

@login_required(login_url='index')
def profile(request, username):
    user = request.user
    previous_url = request.META.get('HTTP_REFERER')
    favorite, created = Wishlist.objects.get_or_create(user=user)
    shelf, created = Shelf.objects.get_or_create(user=user)
    shelfs, created = BorrowedBook.objects.get_or_create(user=user)

    if request.method == 'POST':
        change_password = request.POST.get('change_password') == 'on'
        if change_password:
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            if new_password == confirm_new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed successfully.')
            else:
                messages.error(request, 'New passwords do not match.')
                return redirect(previous_url)
        else:
            # Update other profile fields
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')

        return redirect(previous_url)
    my, _ = BorrowedBook.objects.get_or_create(user=user)
    av = 3 -  my.book.all().count()
    context = {
        'user': user,
        'fav':favorite,
        'shelf':shelf,
        'shelfs':shelfs,
        'my':av
    }
    return render(request, "pages/user/profile.html",context)


@login_required(login_url='index')
def wishlist(request,username):
    user = request.user
    favorite, created = Wishlist.objects.get_or_create(user=user)
    shelf, created = Shelf.objects.get_or_create(user=user)
    shelfs = Wishlist.objects.get(user=user)
    my, _ = BorrowedBook.objects.get_or_create(user=user)
    av = 3 -  my.book.all().count()
    context = {
        'user': user,
        'fav':favorite,
        'shelf':shelf,
        'shelfs':shelfs,
        'my':av,
        'av':my

    }
    return render(request, "pages/user/wishlist.html",context)

@login_required(login_url='index')
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