from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser
from .models import Review

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'username', 'email', 'password1', 'password2',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']