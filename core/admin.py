from django.contrib import admin
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name_link']
    search_fields = ['name__istartswith']
    def name_link(self, genre):
        url = (reverse('admin:core_Book_changelist')
            + '?'
            + urlencode({
                'genre__id': str(genre.id)
            })
        )
        format_html('<a href={}>{}</a>, url, genre')

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author','view', 'status']
    list_filter = ['genres','status', 'author']
    search_fields = ['title__istartswith']


