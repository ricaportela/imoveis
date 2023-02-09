# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import logout as logout_user, login as login_user, authenticate, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from imoveisfinanciados.utils.permissions import LoginRequiredMixin

from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from .models import User


def register(request, template_name='account/register.html'):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data.get('email', None)
            first_name = cleaned_data.get('first_name', None)
            last_name = cleaned_data.get('last_name', None)
            phone = cleaned_data.get('phone', None)
            password = cleaned_data.get('password', None)
            user = User.objects.create_user(
                email, first_name, last_name, phone, password)
            user.save()
            user = authenticate(username=email, password=password)
            login_user(request, user)
            messages.success(
                request, "Bem vindo! Você foi cadastrado com sucesso!")
            return redirect(request.POST.get('next', reverse('realty:user_realties', kwargs={'state': 'br'})))
    else:
        initial = {'email': request.GET.get('email', None)}
        form = RegistrationForm(initial=initial)
    context = {'form': form, 'next': request.GET.get(
        'next', None), 'sidebar_disabled': True}
    return render(request, template_name, context)


def registration_successful(request, template_name='account/registration_successful.html'):
    return render(request, template_name)


def activate(request, template_name='account/activate.html'):
    form = RegistrationForm()
    return render(request, template_name, {'form': form, })


def login(request, template_name='account/login.html'):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, "Você efetuou login com sucesso!")
            state = request.session.get('state', 'br')
            return redirect(request.GET.get('next', reverse('realty:user_realties', kwargs={'state': state})))
        else:
            messages.error(request, "Email e/ou senha inválidos.")
    else:
        form = LoginForm()
    return render(request, template_name, {'form': form, 'sidebar_disabled': True})


def logout(request):
    logout_user(request)
    messages.success(request, "Deslogado com sucesso. Volte sempre!")
    return redirect('index')


def manage(request, template_name='account/manage.html'):
    return render(request, template_name, {})


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = get_user_model()
    form_class = ProfileUpdateForm
    template_name = 'account/profile.html'
    success_message = _("Perfil atualizado com sucesso")

    def get_success_url(self):
        return reverse_lazy('realty:user_realties', kwargs={'state': self.get_user_state()})

    def get_user_state(self):
        return self.request.session.get('state', 'br')

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()

        obj = queryset.get(pk=self.request.user.pk)
        return obj
