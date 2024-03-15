from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'username', 'password1', 'password2',)