from django.shortcuts import render



def profile(request,username):
    return render(request, "pages/user/profile.html",{"username":username})


def wishlist(request,username):
    return render(request, "pages/user/wishlist.html",{"username":username})


def shelf(request,username):
    return render(request, "pages/user/shelf.html",{"username":username})