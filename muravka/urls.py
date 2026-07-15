from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from store.views import (
    home,
    about,
    aromadiagnostics,
    privacy_policy,
    robots_txt
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("robots.txt", robots_txt, name="robots"),
]

urlpatterns += i18n_patterns(
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('store/', include('store.urls')),
    path('aromadiagnostics/', aromadiagnostics, name='aromadiagnostics'),
    path('accounts/', include('allauth.urls')),
    path('privacy/', privacy_policy, name='privacy'),

    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)