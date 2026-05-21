from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from seo.sitemaps import StaticViewSitemap, ProductSitemap
from store.views import home, about, aromadiagnostics, privacy_policy, robots_txt


sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
}

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
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
    path("robots.txt", robots_txt),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)