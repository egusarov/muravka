from django import template
from django.utils.safestring import mark_safe

from store.html_utils import sanitize_product_html

register = template.Library()


@register.filter
def product_html(value):
    """Sanitize a product description before rendering its allowed HTML."""
    return mark_safe(sanitize_product_html(value))
