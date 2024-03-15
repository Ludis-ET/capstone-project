from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required') 

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'username','email', 'password1', 'password2',)