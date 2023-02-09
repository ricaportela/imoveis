# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _


class ContactUsForm(forms.Form):

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
    subject = forms.CharField(
        label=_("Assunto"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Assunto da mensagem")
            }
        ),
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

    def send_mail(self):
        data = self.cleaned_data
        name = data['name']
        email = data['email']
        phone = data['phone']
        subject = u"Imóveis Financiados - Contato: {0}".format(data['subject'])
        message = data['message']
        cc_myself = data['cc_myself']

        html_message = u'''
        <h2>** Contato feito através do site Imoveis Financiados em {0} **</h2>
        <p><strong>Nome</strong>: {1}</p>
        <p><strong>Email</strong>: {2}</p>
        <p><strong>Telefone</strong>: {3}</p>
        <p><strong>Mensagem</strong>: {4}</p>
        '''.format(datetime.now().strftime("%d/%m/%Y - %Hh%M"), name, email, phone, message)

        recipient_list = ["mauriciopublic@hotmail.com", ]

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
