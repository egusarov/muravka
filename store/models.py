import re
from decimal import Decimal

from django.urls import reverse
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language


def validate_image_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError(
            _("Максимальний розмір зображення — 2MB")
        )


def validate_phone(value):
    pattern = r'^(\+380\d{9}|0\d{9})$'
    if not re.match(pattern, value):
        raise ValidationError(
            _("Введіть номер у форматі +380XXXXXXXXX або 0XXXXXXXXX")
        )


class Category(models.Model):
    name = models.CharField(verbose_name=_("Назва"), max_length=200)
    name_ru = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Назва (російською)")
    )

    slug = models.SlugField(verbose_name=_("Slug"), unique=True)

    class Meta:
        verbose_name = _("Категорія")
        verbose_name_plural = _("Категорії")

    @property
    def localized_name(self):
        language = get_language()

        if language.startswith("ru") and self.name_ru:
            return self.name_ru
        return self.name

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name=_("Категорія"),
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name=_("Назва"), max_length=200)
    name_ru = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Назва (російською)")
    )
    slug = models.SlugField(verbose_name=_("Slug"), unique=True)
    description = models.TextField(_("Опис"), blank=True)
    description_ru = models.TextField(
        blank=True,
        verbose_name=_("Опис (російською)")
    )
    price = models.DecimalField(verbose_name=_("Ціна"), max_digits=8, decimal_places=2)
    image = models.ImageField(
        verbose_name=_("Зображення"),
        upload_to='products/',
        validators=[validate_image_size],
        blank=True
    )
    available = models.BooleanField(verbose_name=_("Активний"), default=True)
    created_at = models.DateTimeField(verbose_name=_("Дата створення"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Дата оновлення"), auto_now=True)

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товари")
        ordering = ['-updated_at']

    @property
    def localized_name(self):
        language = get_language()

        if language.startswith("ru") and self.name_ru:
            return self.name_ru

        return self.name

    @property
    def localized_description(self):
        language = get_language()

        if language.startswith("ru") and self.description_ru:
            return self.description_ru

        return self.description

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Користувач"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    first_name = models.CharField(verbose_name=_("Ім'я"), max_length=50)
    last_name = models.CharField(verbose_name=_("Прізвище"), max_length=50)
    phone = models.CharField(verbose_name=_("Мобільний телефон"), max_length=20, validators=[validate_phone])

    city = models.CharField(verbose_name=_("Місто"), max_length=50)
    warehouse = models.CharField(verbose_name=_("Відділення / поштомат"), max_length=255)

    comment = models.TextField(verbose_name=_("Коментар"), blank=True)

    created_at = models.DateTimeField(verbose_name=_("Дата створення"), auto_now_add=True)
    paid = models.BooleanField(verbose_name=_("Оплачено"), default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Замовлення")
        verbose_name_plural = _("Замовлення")

    def get_total_cost(self):
        return sum(
            (item.price * item.quantity for item in self.items.all()),
            Decimal('0')
        )

    def __str__(self):
        return f'Order #{self.id} ({self.first_name} {self.last_name})'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_("Замовлення"),
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Товар"),
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(verbose_name=_("Ціна"), max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name=_("Кількість"), default=1)

    class Meta:
        verbose_name = _("Позиція замовлення")
        verbose_name_plural = _("Позиції замовлення")

    def __str__(self):
        return str(self.id)
