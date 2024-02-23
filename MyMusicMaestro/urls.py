from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('app_pages.urls')),
    path('albums/', include('app_album_viewer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
