from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_author = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_author:
            self.is_staff = True
        if self.is_manager:
            self.is_superuser = True
        super().save(*args, **kwargs)

class Shelf(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    books = models.ManyToManyField('core.Book', related_name='shelves')
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Shelf"

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    books = models.ManyToManyField('core.Book', related_name='wishlists')
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class BorrowedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
