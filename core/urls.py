from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("shelf/",shelf,name='shelf'),
    path("shelf/book/<int:id>",book,name='book'),
    path("register/",register,name='register'),
    path("login/",login,name='login'),
]