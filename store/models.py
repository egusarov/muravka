import re

from django.urls import reverse
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


def validate_image_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Максимальний розмір зображення — 2MB")


def validate_phone(value):
    pattern = r'^(\+380\d{9}|0\d{9})$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Введіть номер у форматі +380XXXXXXXXX або 0XXXXXXXXX'
        )


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', validators=[validate_image_size], blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    first_name = models.CharField("Ім'я", max_length=50)
    last_name = models.CharField("Прізвище", max_length=50)
    phone = models.CharField("Мобільний телефон", max_length=20, validators=[validate_phone])

    city = models.CharField("Місто", max_length=50)
    warehouse = models.CharField("Відділення / поштомат", max_length=255)

    comment = models.TextField("Коментар", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
