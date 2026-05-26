from django.urls import reverse
from store.models import Product


BASE_URL = "https://muravka-krem.pp.ua"


def build_sitemap():
    url_entries = []

    # -------------------------
    # STATIC PAGES
    # -------------------------
    static_pages = [
        "home",
        "about",
        "store:product_list",
        "aromadiagnostics",
    ]

    for page in static_pages:
        url_entries.append({
            "loc": f"{BASE_URL}{reverse(page)}",
            "lastmod": None,
        })

    # -------------------------
    # PRODUCTS
    # -------------------------
    products = Product.objects.filter(available=True)

    for product in products:
        url_entries.append({
            "loc": f"{BASE_URL}{product.get_absolute_url()}",
            "lastmod": product.created_at.date(),
        })

    # -------------------------
    # BUILD XML
    # -------------------------
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