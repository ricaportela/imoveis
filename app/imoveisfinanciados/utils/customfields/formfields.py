from django import forms

from .widgets import RealCurrencyInput


class RealCurrencyField(forms.DecimalField):
    widget = RealCurrencyInput

    def clean(self, value):
        if value:
            value = value.replace('.', '').replace(',', '.')
        return super(RealCurrencyField, self).clean(value)

    def widget_attrs(self, widget):
        return {'class': 'real_currency'}
