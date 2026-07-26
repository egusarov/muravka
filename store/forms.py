from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label=_("Кількість")
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone',
            'city',
            'warehouse',
            'comment'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': _("Ім’я"),
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': _("Прізвище"),
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': _("Телефон"),
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': _("Місто"),
                'class': 'form-control'
            }),
            'warehouse': forms.TextInput(attrs={
                'placeholder': _("Відділення / Поштомат"),
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': _("Коментар до замовлення (необов’язково)"),
                'rows': 3,
                'class': 'form-control'
            })
        }

        error_messages = {
            'first_name': {
                'required': _("Введіть ім’я"),
            },
            'last_name': {
                'required': _("Введіть прізвище"),
            },
            'phone': {
                'required': _("Введіть номер телефону"),
            },
            'city': {
                'required': _("Оберіть місто"),
            },
            'warehouse': {
                'required': _("Оберіть відділення"),
            },
        }
