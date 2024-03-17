from django.contrib import admin
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models

admin.site.register(models.Testimony)

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_list']
    search_fields = ['name']
    def book_list(self, genre):
        url = reverse('admin:core_book_changelist')
        query_params = urlencode({'genres__id__exact': genre.id})
        url += f'?{query_params}'
        return format_html('<a href="{}">{}</a>', url, f'books lists with {genre.name} genre')

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','views', 'status', 'author','borrowed_users_count','average_rating']
    list_filter = ['genres','status', 'author']
    search_fields = ['title__istartswith']
    exclude = ('views', 'status','borrowed_by')

    def borrowed_users_count(self, obj):
        return obj.borrowed_by.count()

    borrowed_users_count.short_description = 'Borrowed Students Count'

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['fields'] = ['title','genres', 'coverpage','book', 'description']
        return super().get_form(request, obj, **kwargs)


    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user and not request.user.is_superuser:
            return False
        return super().has_view_permission(request, obj)
    


