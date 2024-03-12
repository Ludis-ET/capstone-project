from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.ForeignKey(User,on_delete = models.PROTECT)
    genre = models.CharField(max_length=100)
    book = models.FileField(upload_to='books/')
    description = models.TextField()
    history = models.PositiveIntegerField(default = 0)
    status_choices = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='available')

    class Meta:
        unique_together = ("title", "author")
    
    def __str__(self):
        return f'{self.title} book by {self.author.first_name}'
    
    def clean(self):
        if not self.author.is_superuser and not self.author.is_staff:
            raise ValidationError("Only admins and superadmins can add books.")

        max_size = 50 * 1024 * 1024 
        if self.book.size > max_size:
            raise ValidationError("Book size should be less than or equal to 50MB.")
    
class Reveiw(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def clean(self):
        if self.book.status != 'borrowed' or self.user not in self.book.borrowed_by.all():
            raise ValidationError("You can only review books that you have borrowed.")


