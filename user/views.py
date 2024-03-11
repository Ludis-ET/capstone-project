from django.shortcuts import render


def profile(request,username):
    return render(request, "pages/user/profile.html",{})