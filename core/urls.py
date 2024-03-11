from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("shelf/",shelf,name='shelf'),
    path("shelf/book/<int:id>",book,name='book'),
]