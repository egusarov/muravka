from django.contrib import admin
from django import forms
from django.forms.widgets import Textarea
from .models import Category, Product, Order, OrderItem


class JoditWidget(Textarea):
    class Media:
        css = {'all': ('vendor/jodit/jodit.min.css', 'css/jodit-admin.css')}
        js = ('vendor/jodit/jodit.min.js', 'js/jodit-admin.js')

    def __init__(self, attrs=None):
        attrs = {'class': 'vLargeTextField', 'rows': 12, **(attrs or {})}
        super().__init__(attrs)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': JoditWidget(),
            'description_ru': JoditWidget(),
        }

    def clean_description(self):
        from .html_utils import sanitize_product_html
        return sanitize_product_html(self.cleaned_data['description'])

    def clean_description_ru(self):
        from .html_utils import sanitize_product_html
        return sanitize_product_html(self.cleaned_data['description_ru'])


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'available', 'updated_at')
    list_filter = ('category', 'available', 'updated_at')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'updated_at'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'created_at', 'paid']
    inlines = [OrderItemInline]
