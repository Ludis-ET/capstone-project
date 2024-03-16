from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request,username):
    return render(request, "pages/user/profile.html",{"username":username})

@login_required
def wishlist(request,username):
    return render(request, "pages/user/wishlist.html",{"username":username})

@login_required
def shelf(request,username):
    return render(request, "pages/user/shelf.html",{"username":username})