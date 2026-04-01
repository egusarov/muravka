from django.urls import path
from .views import home, product_list, product_detail, cart_detail, cart_add, cart_remove, order_create

app_name = 'store'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('order/create/', order_create, name='order_create'),
]
