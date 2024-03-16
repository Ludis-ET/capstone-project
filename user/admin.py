from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'type_of_user']
    search_fields = ['username__istartswith']
    list_filter = ['is_author', 'is_manager']
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        ("User Identities", {'fields': ('username', 'password', 'is_author', 'is_manager')}),
        ("Additional Identities", {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('groups','is_active',)}),
    )
    add_fieldsets = (
        ("Base Identities", {'fields': ('username', 'password1', 'password2')}),
        ("User Identities", {'fields': ('is_manager', 'is_author', 'is_active')}),
        ("Additional Identities", {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('groups',)}),
    )

    def type_of_user(self, user):
        if not user.is_author and user.is_manager:
            return 'manager'
        if  user.is_author and not user.is_manager:
            return 'author'
        return 'unknown'

