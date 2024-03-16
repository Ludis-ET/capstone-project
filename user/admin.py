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
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'type_of_user']
    search_fields = ['username__istartswith']
    list_filter = ['is_author', 'is_manager']
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        ("user identities", {'fields': ('username', 'password', 'is_author', 'is_manager')}),
        ("additional identities", {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('groups','is_active',)}),
    )
    add_fieldsets = (
        ("Base User", {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username','email', 'password1', 'password2', 'is_author', 'is_manager', 'is_active'),
        }),
    )

    def type_of_user(self, user):
        if user.is_author and user.is_manager:
            return 'manager'
        if user.is_author:
            return 'author'
        return 'unknown'

