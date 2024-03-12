from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.ForeignKey(User,on_delete = models.PROTECT)
    genres = models.ManyToManyField(Genre)
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
        
    @property
    def average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            total_ratings = sum(review.rating for review in reviews)
            return total_ratings / len(reviews)
        else:
            return 0

