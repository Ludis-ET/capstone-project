from django.contrib import admin
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_list']
    search_fields = ['name']
    def book_list(self, genre):
        url = reverse('admin:core_book_changelist')
        query_params = urlencode({'genres__id__exact': genre.id})
        url += f'?{query_params}'
        return format_html('<a href="{}">{}</a>', url, f'{genre.name} Books')

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author','views', 'status']
    list_filter = ['genres','status', 'author']
    search_fields = ['title__istartswith']
    exclude = ('views', 'status')


