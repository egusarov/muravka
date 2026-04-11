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
    from django.conf import settings
    return {
        "GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", None)
    }
