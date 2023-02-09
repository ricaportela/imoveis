# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core import serializers
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
    ListView)
from imoveisfinanciados.realty.models import Realty
from imoveisfinanciados.utils.mixin import JSONResponseMixin
from .forms import ContactUsForm
from .models import State, City


class HomePageView(TemplateView):

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        kwargs = super(HomePageView, self).get_context_data(**kwargs)
        kwargs['sidebar_disabled'] = True
        kwargs['breadcrumbs_disabled'] = True
        return kwargs


class JsonCitiesList(JSONResponseMixin, DetailView):
    """ List all cities from a State """
    model = State

    def options(self, request, *args, **kwargs):
        response = super(JsonCitiesList, self).options(
            request, *args, **kwargs)
        response['Content-type'] = "application/json"
        return response

    def get_context_data(self, **kwargs):
        qs = State.objects.prefetch_related("cities").all()
        obj = self.get_object(queryset=qs)
        context = {
            'object_list': serializers.serialize(
                'json',
                obj.cities.all(),
                fields=('pk', 'name'))
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class ContactUsView(FormView):

    template_name = "core/contactus.html"
    form_class = ContactUsForm

    def get_success_url(self):
        return reverse('contact_us')

    def form_valid(self, form):
        form.send_mail()
        messages.success(
            self.request,
            _("Obrigado! Sua mensagem foi enviada com sucesso!")
        )
        return super(ContactUsView, self).form_valid(form)


class CityListView(ListView):
    model = City

    def get_queryset(self):
        state = self.kwargs['state'].upper()
        return City.objects.filter(state__abbr=state)

    def get_context_data(self, **kwargs):
        kwargs = super(CityListView, self).get_context_data(**kwargs)
        state_req = self.kwargs['state'].upper()
        state = get_object_or_404(State, abbr=state_req)
        kwargs['state'] = state
        return kwargs
