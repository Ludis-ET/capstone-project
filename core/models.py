from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 200)
    cover_page = models.ImageField(upload_to='cover pages/',null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.PROTECT)
    genres = models.ManyToManyField(Genre)
    book = models.FileField(upload_to='books/')
    description = models.TextField()
    history = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='borrowed_books')
    status_choices = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='available')
    date_published = models.DateField(auto_now_add=True,null=True)
    date_updated = models.DateField(auto_now=True,null=True)

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

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField()

    class Meta:
        unique_together = ("book", "user")

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"

    def clean(self):
        if self.user not in self.book.history.all():
            raise ValidationError("You can only review books that you have borrowed.")