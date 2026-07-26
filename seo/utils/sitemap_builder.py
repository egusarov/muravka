from django.conf import settings
from django.urls import reverse
from django.utils.translation import activate

from store.models import Product


BASE_URL = "https://muravka-krem.pp.ua"


def build_sitemap():
    url_entries = []

    default_language = settings.LANGUAGE_CODE

    # --------------------------------------------------
    # Static pages
    # --------------------------------------------------

    untranslated_pages = [
        "home",
        "about",
        "aromadiagnostics",
    ]

    translated_pages = [
        "store:product_list",
    ]

    # Only Ukrainian versions exist
    activate(default_language)

    for page in untranslated_pages:
        url_entries.append({
            "loc": f"{BASE_URL}{reverse(page)}",
            "lastmod": None,
        })

    # Ukrainian + Russian versions
    for language in ("uk", "ru"):
        activate(language)

        for page in translated_pages:
            url_entries.append({
                "loc": f"{BASE_URL}{reverse(page)}",
                "lastmod": None,
            })

    # --------------------------------------------------
    # Products
    # --------------------------------------------------

    products = Product.objects.filter(available=True)

    for language in ("uk", "ru"):
        activate(language)

        for product in products:
            url_entries.append({
                "loc": f"{BASE_URL}{product.get_absolute_url()}",
                "lastmod": product.updated_at.date(),
            })

    # Restore default language
    activate(default_language)

    # --------------------------------------------------
    # Build XML
    # --------------------------------------------------

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    )

    for entry in url_entries:
        xml.append("  <url>")
        xml.append(f"    <loc>{entry['loc']}</loc>")

        if entry["lastmod"]:
            xml.append(f"    <lastmod>{entry['lastmod']}</lastmod>")

        xml.append("  </url>")

    xml.append("</urlset>")

    return "\n".join(xml)