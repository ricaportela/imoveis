from decimal import Decimal

from django import forms
from django.utils.safestring import mark_safe
from .formatters import decimal_to_real


class RealCurrencyInput(forms.TextInput):

    def render(self, name, value, attrs=None, renderer=None):
        value = value or ''
        if isinstance(value, Decimal):
            value = decimal_to_real(str(value), 2)
        attrs = attrs or {}
        attrs['class'] = 'real form-control'
        attrs['alt'] = 'decimal'
        html = super(RealCurrencyInput, self).render(name, value, attrs)
        return mark_safe(html)
