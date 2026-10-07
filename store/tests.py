from decimal import Decimal
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

from .models import Category, Order, Product


@override_settings(
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
)
class TelegramOrderNotificationTests(TestCase):
    def setUp(self):
        social_app = SocialApp.objects.create(
            provider='google',
            name='Google test app',
            client_id='test-client-id',
            secret='test-client-secret',
        )
        social_app.sites.add(Site.objects.get_current())
        category = Category.objects.create(name='Тестова категорія', slug='test-category')
        self.product = Product.objects.create(
            category=category,
            name='Тестовий крем',
            slug='test-cream',
            price=Decimal('125.50'),
            available=True,
        )

    @patch('store.services.telegram.requests.post')
    def test_checkout_sends_order_details_after_saving_order(self, telegram_post):
        telegram_post.return_value = Mock(
            status_code=200,
            json=Mock(return_value={'ok': True}),
        )
        session = self.client.session
        session['cart'] = {
            str(self.product.pk): {'quantity': 2, 'price': str(self.product.price)},
        }
        session.save()

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse('store:order_create'),
                {
                    'first_name': 'Анна',
                    'last_name': 'Тестова',
                    'phone': '+380501234567',
                    'city': 'Київ',
                    'warehouse': 'Відділення №1',
                    'comment': 'Зателефонувати перед відправкою',
                },
            )

        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(first_name='Анна', last_name='Тестова')
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(telegram_post.called)

        payload = telegram_post.call_args.kwargs['json']
        self.assertIn(f'Новый заказ № {order.pk}', payload['text'])
        self.assertIn('Тестовий крем × 2', payload['text'])
        self.assertIn('Тестова Анна', payload['text'])
        self.assertIn('+380501234567', payload['text'])
        self.assertIn('Київ', payload['text'])
        self.assertIn('Відділення №1', payload['text'])
        self.assertIn('Зателефонувати перед відправкою', payload['text'])
        self.assertIn('251.00 грн', payload['text'])
        self.assertIn(f'/admin/store/order/{order.pk}/change/', payload['text'])

    @patch('store.services.telegram.requests.post', side_effect=OSError('Telegram недоступен'))
    def test_telegram_failure_does_not_undo_checkout(self, telegram_post):
        session = self.client.session
        session['cart'] = {
            str(self.product.pk): {'quantity': 1, 'price': str(self.product.price)},
        }
        session.save()

        with self.assertLogs('store.services.telegram', level='ERROR'):
            with self.captureOnCommitCallbacks(execute=True):
                response = self.client.post(
                    reverse('store:order_create'),
                    {
                        'first_name': 'Иван',
                        'last_name': 'Покупатель',
                        'phone': '+380501234567',
                        'city': 'Львів',
                        'warehouse': 'Поштомат №2',
                        'comment': '',
                    },
                )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(first_name='Иван').exists())
        self.assertTrue(telegram_post.called)
