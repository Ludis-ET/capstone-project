from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import Book

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def clean(self):
     # Check if the user has already borrowed 3 books excluding the current instance
        if Borrow.objects.filter(user=self.user).exclude(pk=self.pk).count() >= 3:
            raise ValidationError("You have already borrowed the maximum number of books.")
    