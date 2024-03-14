from django.contrib import admin
from .models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    exclude = ('history',)
    
admin.site.register(Genre)
admin.site.register(Testimony)