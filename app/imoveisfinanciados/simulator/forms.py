from datetime import datetime
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator
from imoveisfinanciados.core.models import State, City
from django.utils.translation import gettext_lazy as _


class IncomeSearchForm(forms.Form):
    year = datetime.now().year
    birth_range = list(reversed(range(year - 70, year - 17)))
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        label=_("Estado"),
        empty_label=_("-- Estado --"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm dynamic-state'}),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        label=_("Cidade"),
        empty_label=_("-- Selecione --"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm dynamic-city'}),
        required=False
    )
    income = forms.DecimalField(
        label=_("Renda"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm income-field',
                'placeholder': 'Sua renda'
            }
        ),
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(600.0))]
    )
    birthday = forms.ChoiceField(
        label=_("Aniversário"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm birthday-field'}),
        choices=[('', 'ANO NASCIMENTO')] + list(zip(birth_range, birth_range)),
    )
    dependents = forms.BooleanField(
        label=_("Dependentes"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(IncomeSearchForm, self).__init__(*args, **kwargs)
        if 'state' in self.data:
            state = self.data['state']
            if state:
                qs = State.objects.prefetch_related("cities").all()
                qs = qs.get(pk=state)
                self.fields['city'].queryset = qs.cities.all()


class InstallmentForm(forms.Form):
    year = datetime.now().year
    birth_range = list(reversed(range(year - 70, year - 17)))
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        label=_("Estado"),
        empty_label=_("-- Estado --"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm dynamic-state'}),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        label=_("Cidade"),
        empty_label=_("-- Selecione --"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm dynamic-city'}),
        required=False
    )
    birthday = forms.ChoiceField(
        label=_("Aniversário"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm birthday-field'}),
        choices=zip(birth_range, birth_range),
    )
    installment = forms.DecimalField(
        label=_("Prestação"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm income-field',
                'placeholder': 'Quer pagar quanto?'
            }
        ),
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(300.0))]
    )
    dependents = forms.BooleanField(
        label=_("Dependentes"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(InstallmentForm, self).__init__(*args, **kwargs)
        if 'state' in self.data:
            state = self.data['state']
            if state:
                qs = State.objects.prefetch_related("cities").all()
                qs = qs.get(pk=state)
                self.fields['city'].queryset = qs.cities.all()
