from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

from .cart import Cart
from .models import Category


def cart(request):
    return {
        'cart': Cart(request)
    }


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def analytics(request):
    return {
        "GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", None)
    }


def language_switcher(request):
    """
    URLs for switching between available languages
    while staying on the current page.
    """
    current_path = request.get_full_path()

    return {
        "switch_to_uk": translate_url(current_path, "uk"),
        "switch_to_ru": translate_url(current_path, "ru"),
    }


def seo_urls(request):
    """
    Canonical and alternate URLs
    for multilingual SEO.
    """
    current_path = request.get_full_path()

    return {
        "canonical_url": request.build_absolute_uri(),
        "alternate_uk": request.build_absolute_uri(
            translate_url(current_path, "uk")
        ),
        "alternate_ru": request.build_absolute_uri(
            translate_url(current_path, "ru")
        ),
        "current_language": get_language(),
    }