# -*- coding: utf-8

from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.translation import gettext_lazy as _

from .models import User


class RegistrationForm(forms.Form):
    """
    Form for registering a new account
    """
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fulano@email.com'}
        )
    )
    first_name = forms.CharField(
        label=_("Nome"),
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    last_name = forms.CharField(
        label=_("Sobrenome"),
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    phone = forms.CharField(
        label=_(u"Telefone"),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '(XX) 2222-2222'}
        )
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Senha"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Confirme sua senha"))

    def clean_email(self):
        """
        Validate that the email doesn't already exist
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u"O endereço de email informado já está em uso"))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verify that the passwords match
        """
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u"As senhas informadas não são idênticas."))
        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone']
        exclude = ['email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        )
    )
    password = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Senha'}
        )
    )
    user = None

    error_messages = {
        'invalid_login': _(u"Informe um email e senha válidos. Lembre-se que \
            as senhas diferenciam maiúsculas de minúsculas."),
        'no_cookies': _(u"Seu navegador está configurado para não aceitar cookies.\
            Habilite os cookies em seu navegador para poder efetuar login."),
        'inactive': _(u"Sua conta está inativa."),
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=self.data['email'],
                                password=self.data['password'])
            if user is not None:
                if user.is_active:
                    self.user = user
                else:
                    raise forms.ValidationError(_(u"Sua conta está temporariamente inativa."))
            else:
                raise forms.ValidationError(_(u"O email e/ou senha informados não são válidos."))

    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            return True
        return False
