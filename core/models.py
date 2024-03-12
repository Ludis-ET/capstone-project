from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Book models to store books details
class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    status_choices = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='available')

    class Meta:
        unique_together = ("title", "author")
    
    def __str__(self):
        return self.title
    
# Review models that user can review a book they borrowed   
class Reveiw(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def clean(self):
        if self.book.status != 'borrowed' or self.user not in self.book.borrowed_by.all():
            raise ValidationError("You can only review books that you have borrowed.")


