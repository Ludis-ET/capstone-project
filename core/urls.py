from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("shelf/",shelf,name='shelf'),
    path("shelf/book/<int:id>",book,name='book'),
    path("register/",register,name='register'),
    path("login/",login,name='login'),
    path("reset/",password_reset_request,name='reset_request'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path("reset-password/<uidb64>/<token>",passwordResetConfirm,name='reset'),
    path("logout/",logout,name='logout'),
    path("activate-request/",activate_request,name='activate_request'),
]