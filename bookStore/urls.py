from django.contrib import admin
from django.urls import path,include

admin.site.site_title = "Djabooks site admin (DEV)"
admin.site.site_header = "Djabooks administration"
admin.site.index_title = "Site administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('<str:username>/',include('user.urls')),
]
