from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from store.views import home, about, aromadiagnostics, privacy_policy, robots_txt


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('store/', include('store.urls')),
    path('aromadiagnostics/', aromadiagnostics, name='aromadiagnostics'),
    # path("massage/", massage, name="massage"),
    path('accounts/', include('allauth.urls')),
    path('privacy/', privacy_policy, name='privacy'),

    # SEO
    path("robots.txt", robots_txt, name="robots"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)