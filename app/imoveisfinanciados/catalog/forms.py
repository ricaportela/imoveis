# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django import forms
from django.utils.translation import gettext_lazy as _
from imoveisfinanciados.core.models import City, State
from imoveisfinanciados.realty.forms import AdvertiserContactForm
from .models import Catalog, CatalogPhone, CatalogType


class CatalogForm(forms.ModelForm):

    city = forms.ModelChoiceField(
        label=_("Cidade"),
        queryset=City.objects.none(),
        empty_label=_("-- Selecione --"),
        widget=forms.Select(attrs={'class': 'form-control dynamic-city'})
    )

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._type = "ctype" in kwargs and kwargs.pop('ctype') or None
        super(CatalogForm, self).__init__(*args, **kwargs)
        if kwargs['instance']:  # for Update
            state = kwargs['instance'].state.pk
            qs = State.objects.prefetch_related("cities").all()
            qs = qs.get(pk=state)
            self.fields['city'].queryset = qs.cities.all()

    class Meta:
        model = Catalog
        fields = (
            'name', 'localization', 'email', 'state', 'city', 'logo',
        )
        exclude = ['user', 'created', 'modified', 'slug', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'localization': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control dynamic-state'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        obj = super(CatalogForm, self).save(commit=False)
        obj.user = self._user
        if self._type:
            obj.type = CatalogType.objects.get(type=self._type)
        if commit:
            obj.save()
        return obj


class CatalogPhoneForm(forms.ModelForm):

    class Meta:
        model = CatalogPhone
        fields = (
            'type', 'number'
        )
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control phone-mask'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }


class CatalogEmail(AdvertiserContactForm):

    def html_message(self, name, email, phone, interest, url, msg):
        html_message = u'''
        <h2>** Contato feito através do site Imoveis Financiados em {0} **</h2>
        <p><strong>Nome</strong>: {1}</p>
        <p><strong>Email</strong>: {2}</p>
        <p><strong>Telefone</strong>: {3}</p>
        <p><strong>Catálogo</strong>: <a href="{5}" title="{4}">{4}</a></p>
        <p><strong>Mensagem</strong>: {6}</p>
        '''.format(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"), name, email, phone, interest, url, msg)
        return html_message
