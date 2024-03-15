from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token


def index(request):
    return render(request, "pages/Home/home.html",{})


def activateEmail(request,user,to):
    mail_subject = "Activate Your Email Account"
    message = render_to_string('email/activate.html', {
        "user": user,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else "http"
    })
    email = EmailMessage(mail_subject, message, [to])
    if email.send():
        messages.success(request, f'{user} account created successfully! check <b>{to}</b> and confirm your account')
    else:
        messages.error(request, f'problem sending email to <b>{to}</b> please try again ')

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
    # books = Book.objects.all()
    return render(request, "pages/shelf/shelf.html",{})


def book(request,id):
    return render(request, "pages/shelf/BookDetail.html",{})
