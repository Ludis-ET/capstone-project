from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import *


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    list_display = ["is_author" ]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_author', 'is_manager')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        ("Base User", {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_author', 'is_manager', 'is_active'),
        }),
    )
