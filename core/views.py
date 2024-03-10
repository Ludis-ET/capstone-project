from django.shortcuts import render

def index(request):
    return render(request, "pages/Home/home.html",{})


def shelf(request):
    return render(request, "components/link.html",{})
