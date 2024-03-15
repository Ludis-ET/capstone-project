<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
=======
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
>>>>>>> 228ff23407da50740c0b2fe232f2e0ee74b54fd5
        fields = ('first_name', 'username', 'password1', 'password2',)