from django import forms
from .models import Order


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Кількість'
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
                'placeholder': "Ім’я",
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': "Прізвище",
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': "Телефон",
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': "Місто",
                'class': 'form-control'
            }),
            'warehouse': forms.TextInput(attrs={
                'placeholder': "Відділення / Поштомат",
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': "Коментар до замовлення (необов’язково)",
                'rows': 3,
                'class': 'form-control'
            })
        }

        error_messages = {
            'first_name': {
                'required': "Введіть ім’я",
            },
            'last_name': {
                'required': "Введіть прізвище",
            },
            'phone': {
                'required': "Введіть номер телефону",
            },
            'city': {
                'required': "Оберіть місто",
            },
            'warehouse': {
                'required': "Оберіть відділення",
            },
        }
