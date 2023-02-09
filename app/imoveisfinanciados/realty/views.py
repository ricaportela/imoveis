# -*- coding: utf-8 -*-

import json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, FormView, DetailView
from extra_views import InlineFormSetView, CreateWithInlinesView, UpdateWithInlinesView

from imoveisfinanciados.core.mixin import StateListMixin
from imoveisfinanciados.core.models import City
from imoveisfinanciados.simulator.forms import IncomeSearchForm, InstallmentForm
from imoveisfinanciados.simulator.incomesimulator import IncomeSimulator
from imoveisfinanciados.simulator.installmentsimulator import InstallmentSimulator
from imoveisfinanciados.utils.mixin import JSONResponseMixin
from imoveisfinanciados.utils.money import clean_money, Money
from imoveisfinanciados.utils.permissions import LoginRequiredMixin
from .forms import (
    RealtyForm,
    PhotoForm,
    AdvertiserContactForm,
    AdvancedSearchForm,
)
from .models import Realty, Photo


class RealtyAdvancedSearch(ListView):
    model = Realty
    money_fields = ["min_value", "max_value"]
    paginate_by = 10

    def _update_money_fields(self, data):
        for k, v in data.items():
            if k in self.money_fields:
                data[k] = clean_money(v)
        return data

    def get_context_data(self, **kwargs):
        kwargs = super(RealtyAdvancedSearch, self).get_context_data(**kwargs)
        filter = self.request.GET.dict()

        if 'csrfmiddlewaretoken' in filter:
            filter.pop('csrfmiddlewaretoken')

        if 'page' in filter:
            filter.pop('page')

        from urllib.parse import urlencode
        kwargs['filtering'] = urlencode(filter)

        return kwargs

    def get_queryset(self):
        qs = super(RealtyAdvancedSearch, self).get_queryset()

        data_ = self.request.GET.dict()
        data = self._update_money_fields(data_)

        form = AdvancedSearchForm(data)
        if form.is_valid():
            cleaned = form.cleaned_data
            for key, value in data.items():
                if value:
                    if key == 'keyword':
                        qs = qs.filter(
                            Q(title__icontains=cleaned["keyword"]) |
                            Q(description__icontains=cleaned["keyword"])
                        )
                    if key == 'max_value':
                        qs = qs.filter(value__lte=cleaned["max_value"])
                    if key == 'min_value':
                        qs = qs.filter(value__gte=cleaned["min_value"])
                    if key == 'type' and (cleaned['type'] != 'all'):
                        qs = qs.filter(type=cleaned["type"])
                    if key == 'state':
                        qs = qs.filter(state=cleaned['state'])
                    if key == 'city':
                        qs = qs.filter(city=cleaned['city'])
        return qs


class InstallmentSearch(ListView):
    model = Realty
    money_fields = ['installment']
    paginate_by = 10

    def _simulation(self, installment, city, birth, dependents):
        simulator = InstallmentSimulator(installment)
        income = simulator.calc()
        if 'price' in income:
            income_simulator = IncomeSimulator(
                city, income['price'], birth, dependents)
            return dict(simulator=income_simulator.calc(), installment=income, searched=installment)
        else:
            return {}

    def _update_money_fields(self, data):
        for k, v in data.items():
            if k in self.money_fields:
                #data[k] = clean_money(v)
                data[k] = (v)
        return data

    def get_queryset(self):
        qs = super(InstallmentSearch, self).get_queryset()

        data_ = self.request.GET.dict()
        data = self._update_money_fields(data_)

        form = InstallmentForm(data)
        if form.is_valid():
            cleaned = form.cleaned_data
            for key, value in data.items():
                if value:
                    if key == 'state':
                        qs = qs.filter(state=cleaned['state'])
                    if key == 'city':
                        qs = qs.filter(city=cleaned['city'])
            self.simulator = self._simulation(
                cleaned['installment'],
                cleaned['city'],
                cleaned['birthday'],
                cleaned['dependents'],
            )

        return qs

    def get_context_data(self, **kwargs):
        kwargs = super(InstallmentSearch, self).get_context_data(**kwargs)
        filter = self.request.GET.dict()

        if 'search_type' in filter:
            kwargs['search_type'] = filter['search_type']

        if 'csrfmiddlewaretoken' in filter:
            filter.pop('csrfmiddlewaretoken')

        if 'page' in filter:
            filter.pop('page')

        from urllib.parse import urlencode
        kwargs['filtering'] = urlencode(filter)

        if hasattr(self, 'simulator'):
            kwargs['simulator'] = self.simulator['simulator']
            kwargs['installment'] = self.simulator['installment']
            kwargs['searched'] = self.simulator['searched']

        return kwargs


class RealtyIncomeSearch(ListView):

    model = Realty
    money_fields = ["income", ]
    paginate_by = 10

    def _simulation(self, city, income, birth, dependents):
        simulator = IncomeSimulator(city, income, birth, dependents)
        return dict(simulator=simulator.calc())

    def _update_money_fields(self, data):
        for k, v in data.items():
            if k in self.money_fields:
                #data[k] = clean_money(v)  
                data[k] = (v)  
        return data

    def get_context_data(self, **kwargs):
        kwargs = super(RealtyIncomeSearch, self).get_context_data(**kwargs)
        filter = self.request.GET.dict()

        if 'csrfmiddlewaretoken' in filter:
            filter.pop('csrfmiddlewaretoken')

        if 'page' in filter:
            filter.pop('page')

        from urllib.parse import urlencode
        kwargs['filtering'] = urlencode(filter)

        if hasattr(self, 'simulator'):
            kwargs['simulator'] = self.simulator['simulator']

        return kwargs

    def get_queryset(self):
        qs = super(RealtyIncomeSearch, self).get_queryset()

        data_ = self.request.GET.dict()
        data = self._update_money_fields(data_)

        form = IncomeSearchForm(data)
        if form.is_valid():
            cleaned = form.cleaned_data
            for key, value in data.items():
                if value:
                    if key == 'state':
                        qs = qs.filter(state=cleaned['state'])
                    if key == 'city':
                        qs = qs.filter(city=cleaned['city'])
            self.simulator = self._simulation(
                cleaned['city'],
                cleaned['income'],
                cleaned['birthday'],
                cleaned['dependents'],
            )

        return qs


class RealtyPhotosFormSet(InlineFormSetView):
    model = Photo
    form_class = PhotoForm
    extra = 1
    max_num = 7


class RealtyListView(StateListMixin, ListView):

    model = Realty
    paginate_by = 10

    def get_queryset(self):
        queryset = super(RealtyListView, self).get_queryset()
        queryset = queryset.select_related("state")
        state = str(self.kwargs['state'])
        if state:
            self.request.session.set_expiry(0)
            self.request.session['state'] = state
            queryset = queryset.filter(state__abbr__iexact=state)
        if self.request.GET.get('ordering') == u'date':
            queryset = queryset.order_by('-modified')
        return queryset


class UserRealtyListView(LoginRequiredMixin, ListView):
    """ Listagem dos imóveis no painel do usuário
    """
    model = Realty
    template_name = "realty/userrealty_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super(UserRealtyListView, self).get_queryset()
        queryset = queryset.filter(user__exact=self.request.user.pk)
        return queryset


class RealtyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateWithInlinesView):

    model = Realty
    form_class = RealtyForm
    inlines = [RealtyPhotosFormSet, ]
    success_message = "Imóvel cadastrado com sucesso!"

    def get_success_url(self):
        # return reverse('realty:user_realties', kwargs={'state': 'br'})
        return reverse('myrealties:user_realties')

    def get_form_kwargs(self):
        kwargs = super(RealtyCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_form(self, form_class=None):
        form = super(RealtyCreateView, self).get_form(form_class)
        kwargs = self.get_form_kwargs()
        if "data" in kwargs:
            data = kwargs['data'].dict()
            city = data['city']
            if not city:
                return form
            form.fields['city'].queryset = City.objects.filter(pk__exact=city)
        return form


class RealtyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateWithInlinesView):

    model = Realty
    form_class = RealtyForm
    inlines = [RealtyPhotosFormSet, ]
    success_message = "Imóvel atualizado com sucesso!"

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponse("Unauthorized", 401)
        return super(RealtyUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # return reverse('realty:user_realties', kwargs={'state': 'br'})
        return reverse('myrealties:user_realties')

    def get_form_kwargs(self):
        kwargs = super(RealtyUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_form(self, form_class=None):
        form = super(RealtyUpdateView, self).get_form(form_class)
        kwargs = self.get_form_kwargs()
        if "data" in kwargs:
            data = kwargs['data'].dict()
            city = data['city']
            form.fields['city'].queryset = City.objects.filter(pk__exact=city)
        return form


class RealtyDetailView(FormView):

    model = Realty
    template_name = "realty/realty_detail.html"
    form_class = AdvertiserContactForm

    def get_success_url(self):
        return reverse('realty:view', kwargs={'slug': self.get_object.slug})

    @property
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        kwargs = super(RealtyDetailView, self).get_context_data(**kwargs)
        kwargs['object'] = self.get_object
        return kwargs

    def form_valid(self, form):
        obj = self.get_object
        url = reverse("realty:view", kwargs={'slug': obj.slug})
        fullpath = "".join(
            ["http://", get_current_site(self.request).domain, url])
        form.send_mail(obj.user.email, obj.title, fullpath)
        messages.success(
            self.request,
            _(u"Obrigado! Sua mensagem foi enviada com sucesso!")
        )
        return super(RealtyDetailView, self).form_valid(form)


class UserNumberJson(JSONResponseMixin, DetailView):
    """ Get phone number of an user """

    model = Realty

    def options(self, request, *args, **kwargs):
        response = super(UserNumberJson, self).options(
            request, *args, **kwargs)
        response['Content-type'] = "application/json"
        return response

    def get_context_data(self, **kwargs):
        qs = self.get_object()
        result = {"phone": qs.user.phone}
        context = {
            'advertiser_number': json.dumps(result)
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class CityDetailView(DetailView):
    model = City
    template_name = 'realty/realty_list.html'

    def get_context_data(self, **kwargs):
        kwargs = super(CityDetailView, self).get_context_data(**kwargs)
        kwargs['object_list'] = Realty.objects.filter(city=self.object.pk)
        kwargs['state_meta'] = self.object.state
        return kwargs
