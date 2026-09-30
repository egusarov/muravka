import re
from html import escape

import nh3


PRODUCT_HTML_TAGS = {
    'a', 'blockquote', 'br', 'code', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
    'li', 'ol', 'p', 's', 'strong', 'sub', 'sup', 'ul',
}
PRODUCT_HTML_ATTRIBUTES = {
    'a': {'href', 'title'},
    'blockquote': {'style'},
    'li': {'style'},
    'p': {'style'},
    'h1': {'style'},
    'h2': {'style'},
    'h3': {'style'},
    'h4': {'style'},
    'h5': {'style'},
    'h6': {'style'},
}
TEXT_ALIGNMENTS = {'left', 'right', 'center', 'justify', 'start', 'end'}


def filter_product_attribute(tag, attribute, value):
    """Preserve only recognized text alignment from Jodit's inline styles."""
    if attribute != 'style':
        return value

    for declaration in value.split(';'):
        name, separator, setting = declaration.partition(':')
        if separator and name.strip().lower() == 'text-align':
            alignment = setting.strip().lower()
            if alignment in TEXT_ALIGNMENTS:
                return f'text-align:{alignment}'
    return None


def sanitize_product_html(value):
    """Keep only the formatting supported by the product description editor."""
    value = value or ''
    # Preserve the formatting of descriptions saved before the HTML editor existed.
    if not re.search(r'<\s*[a-zA-Z][^>]*>', value):
        return '<br>'.join(escape(line) for line in value.splitlines())
    return nh3.clean(
        value,
        tags=PRODUCT_HTML_TAGS,
        attributes=PRODUCT_HTML_ATTRIBUTES,
        attribute_filter=filter_product_attribute,
        filter_style_properties={'text-align'},
        url_schemes={'http', 'https', 'mailto'},
        link_rel='nofollow noopener noreferrer',
    )
