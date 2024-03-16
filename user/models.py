from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_author = models.BooleanField(default=False, verbose_name= "is an Author")
    is_manager = models.BooleanField(default=False, verbose_name= "is a Manager")

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def save(self, *args, **kwargs):
        if self.is_author and not self.is_manager:
            self.is_staff = True
            self.is_superuser = False
        elif self.is_manager and not self.is_author:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = self.is_author
            self.is_superuser = self.is_manager
        super().save(*args, **kwargs)


class Shelf(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name = "Student")
    books = models.ManyToManyField('core.Book', related_name='shelves',blank = True)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Shelf"

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    books = models.ManyToManyField('core.Book', related_name='wishlists',blank = True)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class BorrowedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
