"""
URL configuration for intellisoft project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Serve media and static files in development (must be registered before website catch-all)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if getattr(settings, 'STATICFILES_DIRS', None):
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

urlpatterns += [
    path('', include('website.urls')),
]

# Global HTTP Error Handlers
handler400 = 'website.views.error_400'
handler403 = 'website.views.error_403'
handler404 = 'website.views.error_404'
handler500 = 'website.views.error_500'

