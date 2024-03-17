from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse

from user.models import CustomUser,Wishlist,Shelf
from .models import *
from .forms import CustomUserCreationForm, ReviewForm
from .token import account_activation_token

# django orm



def activate(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('index')

def index(request):
    user = request.user
    demanding_books = Book.objects.annotate(borrowed_users_count=Count('borrowed_by')).order_by('-borrowed_users_count')
    latest_books = Book.objects.all().order_by('-date_updated')
    featured_books = Book.objects.all().order_by('-views')
    testimonies = Testimony.objects.all()
    if user.is_authenticated:
        favorite, created = Wishlist.objects.get_or_create(user=user)
        shelf, created = Shelf.objects.get_or_create(user=user)
    else:
        favorite = shelf = None
    context = {
        'user': user,
        'demanding':demanding_books,
        'latest':latest_books,
        'featured':featured_books,
        'fav':favorite,
        'shelf':shelf,
        'tes':testimonies
    }
    return render(request, "pages/Home/home.html", context)


def activateEmail(request,user,to):
    mail_subject = "Activate Your Email Account"
    message = render_to_string('email/activation.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    
    try:
        send_mail(mail_subject, message, None, [to], html_message=message)
        messages.success(request, f"{user}'s account is created successfully! Check {to} and confirm your account.")
    except Exception as e:
        messages.error(request, f'Problem sending email to <b>{to}</b>. Please try again. Error: {str(e)}')

def register(request):
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
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
    user = request.user
    books_list = Book.objects.all()
    genres = Genre.objects.all()

    genre_filter = request.GET.getlist('genre')
    availability_filter = request.GET.getlist('availability')
    rating_filter = request.GET.get('rating')

    sort_by = request.GET.get('sort')
    if sort_by == 'p-name':
        books_list = sorted(books_list, key=lambda x: x.borrowed_by.count(), reverse=True)

    if genre_filter:
        for genre in genre_filter:
            books_list = books_list.filter(genres__name=genre)

    if availability_filter:
        books_list = books_list.filter(status__in=availability_filter)

    if rating_filter:
        rating_value = int(rating_filter[:-1])
        books_list = [book for book in books_list if book.average_rating >= rating_value]

    items_per_page = int(request.GET.get('number', 6))
    paginator = Paginator(books_list, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if user.is_authenticated:
        favorite, created = Wishlist.objects.get_or_create(user=user)
        shelf, created = Shelf.objects.get_or_create(user=user)
    else:
        favorite = shelf = None

    context = {
        'user': user,
        'fav': favorite,
        'shelf': shelf,
        'books': page_obj,
        'items_per_page': items_per_page,
        'genres': genres,
        'genre_filter': genre_filter,
        'availability_filter': availability_filter,
        'rating_filter': rating_filter,
    }
    return render(request, "pages/shelf/shelf.html", context)



def book(request,id):
    user = request.user
    book = Book.objects.get(id=id)
    favorite, created = Wishlist.objects.get_or_create(user=user)
    shelf, created = Shelf.objects.get_or_create(user=user)
    reviews = Review.objects.filter(book=book)
    recommended_books = Book.objects.filter(genres__in=book.genres.all()).exclude(id=book.id).distinct()[:5]
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = user
            review.save()
            messages.success(request, 'Review posted successfully! Thank you.')
            return redirect(reverse('book', kwargs={'id': book.id}))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error} on {field}')
        return redirect(reverse('book', kwargs={'id': book.id}))
    else:
        book.views += 1
        book.save()
                
    context = {
        'user': user,
        'fav':favorite,
        'shelf':shelf,
        'book':book,
        'reviews':reviews,
        'rec':recommended_books,
    }
    return render(request, "pages/shelf/BookDetail.html",context)


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = CustomUser.objects.filter(Q(email=user_email)).first()
            if associated_user:
                mail_subject = "Password Reset Link"
                message = render_to_string('email/reset.html', {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                
                try:
                    send_mail(mail_subject, message, None, [user_email], html_message=message)
                    messages.success(request, f'A password reset link sent to your address! Check {user_email} and confirm reset your password.')
                except Exception as e:
                    messages.error(request, f'Problem sending email to <b>{user_email}</b>. Please try again. Error: {str(e)}')
            
            else:messages.error(request, f'email not found')
    return redirect('index')



def passwordResetConfirm(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in now.")
                return redirect('index')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f' {error}')

        return render(request, 'pages/user/resetpassword.html',{})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("index")


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Leaving so soon? Don't worry, we'll keep your virtual seat warm for when you decide to return! 👋😄")
    return redirect('shelf')