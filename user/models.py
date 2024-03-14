from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.conf import settings


class CustomUser(AbstractUser):
    is_author = models.BooleanField(default=False, verbose_name=_("Make User an Author"))
    is_manager = models.BooleanField(default=False, verbose_name=_("Make User a Manager"))
    email_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the user is being created
            self.is_active = False  # Deactivate user until email is verified
            verification_token = get_random_string(length=32)
            self.send_email_verification(verification_token)
        self.is_staff = self.is_author
        self.is_superuser = self.is_manager
        super().save(*args, **kwargs)

    def send_email_verification(self, token):
        subject = _('Email Verification')
        message = f'Click the link below to verify your email address:\n\nhttp://example.com/verify/{token}/'
        send_mail(subject, message, 'from@example.com', [self.email])

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")


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
