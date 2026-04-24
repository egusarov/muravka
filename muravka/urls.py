from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from store.views import home, about, aromadiagnostics, privacy_policy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('aromadiagnostics/', aromadiagnostics, name='aromadiagnostics'),
    path('store/', include('store.urls')),
    path('accounts/', include('allauth.urls')),
    path('privacy/', privacy_policy, name='privacy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)