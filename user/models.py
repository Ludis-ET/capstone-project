from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    is_author = models.BooleanField(default=False, verbose_name= "Make User an Author")
    is_manager = models.BooleanField(default=False, verbose_name= "Make User a Manager")

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def save(self, *args, **kwargs):
        self.is_staff = self.is_author
        self.is_superuser = self.is_manager
        super().save(*args, **kwargs)


class Shelf(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name = "Student")
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
