from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .token import account_activation_token
from user.models import CustomUser

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
    return render(request, "pages/Home/home.html",{})


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
        messages.success(request, f'{user} account created successfully! Check {to} and confirm your account.')
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
    # books = Book.objects.all()
    return render(request, "pages/shelf/shelf.html",{})


def book(request,id):
    return render(request, "pages/shelf/BookDetail.html",{})
