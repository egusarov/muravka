import html
import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


def build_order_message(order, admin_url):
    """Build an HTML-formatted Telegram message for an order."""
    items = order.items.select_related('product').all()
    item_lines = [
        f"• {html.escape(item.product.localized_name)} × {item.quantity}"
        for item in items
    ]

    message = [
        f"🛍 <b>Нове замовлення № {order.pk}</b>",
        "",
        *item_lines,
        "",
        f"💎 {order.get_total_cost():.2f} грн",
        "",
        f"👤 {html.escape(order.last_name)} {html.escape(order.first_name)}",
        f"📞️ {html.escape(order.phone)}",
        f"🗺 {html.escape(order.city)}",
        f"🚚 {html.escape(order.warehouse)}",
        f"💬 {html.escape(order.comment) if order.comment else '—'}",
        "",
        f'<a href="{html.escape(admin_url, quote=True)}">Відкрити замовлення</a>',
    ]
    return "\n".join(message)


def send_order_notification(order, admin_url):
    """Send the order message; log errors without affecting order processing."""
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    if not bot_token or not chat_id:
        logger.error("Telegram order notification is not configured (order_id=%s)", order.pk)
        return False

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': build_order_message(order, admin_url),
            'parse_mode': 'HTML',
            'disable_web_page_preview': True,
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        if not result.get('ok'):
            logger.error("Telegram rejected order notification (order_id=%s)", order.pk)
            return False
    except Exception as exc:
        logger.exception(
            "Failed to prepare or send Telegram order notification (order_id=%s): %s",
            order.pk,
            exc,
        )
        return False

    return True
