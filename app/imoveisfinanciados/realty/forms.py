# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal

from django import forms
from django.core.mail import EmailMultiAlternatives
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from imoveisfinanciados.core.models import City, State
from imoveisfinanciados.utils.customfields.formfields import RealCurrencyField
from .models import Realty, Photo


class AdvancedSearchForm(forms.Form):
    """ """
    TYPES = (
        ("all", _("Todos")),
        ("apt", _("Apartamento")),
        ("casa", _("Casa")),
        ("cond", _("Condomínio"))
    )

    keyword = forms.CharField(
        label=_("Palavra-chave"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': "Palavra-chave"
            }
        ),
        required=False,
    )
    min_value = forms.DecimalField(
        label=_("Preço mínimo"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': ' Preço mínimo'
            }
        ),
        max_digits=9,
        decimal_places=2,
        required=False,
    )
    max_value = forms.DecimalField(
        label=_("Preço máximo"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Preço máximo'
            }
        ),
        max_digits=9,
        decimal_places=2,
        required=False,
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        label=_("Estado"),
        empty_label=_("-- Estado --"),
        widget=forms.Select(attrs={'class': 'form-control input-sm dynamic-state'}),
        required=False,
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        label=_("Cidade"),
        empty_label=_("-- Selecione --"),
        widget=forms.Select(attrs={'class': 'form-control input-sm dynamic-city'}),
        required=False
    )
    type = forms.ChoiceField(
        label=_("Tipo"),
        choices=TYPES,
        widget=forms.Select(attrs={'class': 'form-control input-sm'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        if 'state' in self.data:
            state = self.data['state']
            if state:
                qs = State.objects.prefetch_related("cities").all()
                qs = qs.get(pk=state)
                self.fields['city'].queryset = qs.cities.all()


class AdvertiserContactForm(forms.Form):

    name = forms.CharField(
        label=_("Nome"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Seu nome")
            },
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Seu e-mail")
            }
        )
    )
    phone = forms.CharField(
        label=_("Telefone"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Seu telefone (opcional)")
            }
        ),
        required=False
    )
    message = forms.CharField(
        label=_("Mensagem"),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _("Mensagem")
            }
        )
    )
    cc_myself = forms.BooleanField(label="Envie-me uma cópia", required=False)

    def html_message(self, name, email, phone, interest, url, msg):
        html_message = u'''
        <h2>** Contato feito através do site Imoveis Financiados em {0} **</h2>
        <p><strong>Nome</strong>: {1}</p>
        <p><strong>Email</strong>: {2}</p>
        <p><strong>Telefone</strong>: {3}</p>
        <p><strong>Imóvel de interesse</strong>: <a href="{5}" title="{4}">{4}</a></p>
        <p><strong>Mensagem</strong>: {6}</p>
        '''.format(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"), name, email, phone, interest, url, msg)
        return html_message

    def send_mail(self, to, interest, url):
        data = self.cleaned_data
        name = data['name']
        email = data['email']
        phone = data['phone']
        subject = "Imóveis Financiados - Contato: {0}".format(data['name'])
        message = data['message']
        cc_myself = data['cc_myself']

        html_message = self.html_message(name, email, phone, interest, url, message)

        recipient_list = [to, ]

        maildata = {
            'subject': subject,
            'body': message,
            'to': recipient_list,
            'headers': {'Reply-To': email}
        }

        if cc_myself:
            maildata.update({'cc': [email, ]})

        email_ = EmailMultiAlternatives(**maildata)
        email_.encoding = "utf-8"
        email_.attach_alternative(html_message, "text/html")
        email_.send()
        return


class RealtyForm(forms.ModelForm):

    city = forms.ModelChoiceField(
        label=_("Cidade"),
        queryset=City.objects.none(),
        empty_label=_("-- Selecione --"),
        widget=forms.Select(attrs={'class': 'form-control dynamic-city'})
    )

    value = RealCurrencyField(
        label=_(u"Preço"),
        max_digits=9,
        decimal_places=2,
    )

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(RealtyForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:  # for Update
            instance = kwargs['instance']
            if instance:
                state = instance.state.pk
                qs = State.objects.prefetch_related("cities").all()
                qs = qs.get(pk=state)
                self.fields['city'].queryset = qs.cities.all()

    class Meta:
        model = Realty
        fields = (
            'title', 'description', 'type', 'state',
            'city', 'value', 'bedroom', 'bathroom', 'size', 'main_image'
        )
        exclude = ['user', 'created', 'modified', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control dynamic-state'}),
            'bedroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        obj = super(RealtyForm, self).save(commit=False)
        obj.user = self._user
        if commit:
            obj.save()
        return obj


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('image', )
        exclude = ('title', )
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
