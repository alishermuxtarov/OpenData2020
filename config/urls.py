from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

from rest_framework.documentation import include_docs_urls
from rest_framework import permissions


permissions_list = [permissions.AllowAny if settings.DEBUG else permissions.IsAuthenticated]

urlpatterns = [
    path('', include([
        path('docs/', include_docs_urls(
            title='API Documentation',
            permission_classes=permissions_list,
        )),
        path('auth/', include(('authentication.urls', 'authentication'), namespace='authentication')),
        path('vehicle/', include(('vehicle.urls', 'vehicle'), namespace='vehicle')),
    ])),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
