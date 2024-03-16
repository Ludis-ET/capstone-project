from django.urls import path
from .views import *

urlpatterns = [
    path("profile/",profile,name='profile'),
    path("wishlist/",wishlist,name='wishlist'),
    path("shelf/",shelf,name='myshelf'),
    path("add-to-wishlist/<int:id>",add_wishlist,name='addwish'),
    path("remove-from-wishlist/<int:id>",remove_wishlist,name='remwish'),
    path("add-to-shelf/<int:id>",add_shelf,name='addshelf'),
    path("add-to-borrow/<int:id>",add_borrow,name='addborrow'),
    path("remove-from-shelf/<int:id>",remove_shelf,name='remshelf'),
    path("remove-from-book/<int:id>",remove_book,name='rembook'),
]