from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model  # Import get_user_model

User = get_user_model()  # Get the user model dynamically

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    coverpage = models.ImageField(upload_to='coverpages/', null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)  # Use the dynamically retrieved User model
    genres = models.ManyToManyField(Genre)
    book = models.FileField(upload_to='books/')
    description = models.TextField()
    history = models.ManyToManyField(User, related_name='borrowed_books', blank=True)
    views = models.PositiveIntegerField(default=0)
    status_choices = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='available')
    date_published = models.DateField(auto_now_add=True, null=True)
    date_updated = models.DateField(auto_now=True, null=True)

    class Meta:
        unique_together = ("title", "author")
    
    def __str__(self):
        return f'{self.title} book by {self.author.first_name}'
    
    def clean(self):
        max_size = 500 * 1024 * 1024 
        if self.book.size > max_size:
            raise ValidationError("Book size should be less than or equal to 500MB.")
        
    @property
    def average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            total_ratings = sum(review.rating for review in reviews if review.book == self)
            return int(total_ratings / len(reviews))
        else:
            return 0
    
    @property
    def total_rating(self):
        return self.review_set.all().count()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField()
    date_rated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("book", "user")

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"

class Testimony(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Testimonies"

    def __str__(self):
        return f"message from {self.author.first_name}"
