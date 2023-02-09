# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic
from extra_views import InlineFormSetView, CreateWithInlinesView, UpdateWithInlinesView
from imoveisfinanciados.core.mixin import StateListMixin
from imoveisfinanciados.core.models import City
from imoveisfinanciados.utils.permissions import LoginRequiredMixin
from .forms import CatalogForm, CatalogPhoneForm, CatalogEmail
from .models import Catalog, CatalogPhone


class CatalogChoiceType(LoginRequiredMixin, generic.TemplateView):
    """
    """
    template_name = "catalog/catalog_type.html"


class CatalogListView(StateListMixin, generic.ListView):
    """
    """
    model = Catalog
    paginate_by = 10
    catalog_type = None

    def get_context_data(self, **kwargs):
        kwargs = super(CatalogListView, self).get_context_data(**kwargs)
        kwargs['catalog_type'] = self.catalog_type
        return kwargs

    def get_queryset(self):
        qs = getattr(Catalog.objects, self.catalog_type)
        return qs()


class CatalogPhonesFormSet(InlineFormSetView):
    model = CatalogPhone
    form_class = CatalogPhoneForm
    extra = 1
    max_num = 4


class CatalogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateWithInlinesView):

    model = Catalog
    form_class = CatalogForm
    inlines = [CatalogPhonesFormSet, ]
    success_message = "Catálogo cadastrado com sucesso!"
    ctype = None

    def get_success_url(self):
        return reverse('catalog:detail', kwargs={'pk': self.object.pk})
        # return reverse('catalog:user_list')

    def get_form_kwargs(self):
        kwargs = super(CatalogCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user, "ctype": self.ctype})
        return kwargs

    def get_form(self, form_class=None):
        form = super(CatalogCreateView, self).get_form(form_class)
        kwargs = self.get_form_kwargs()
        if "data" in kwargs:
            data = kwargs['data'].dict()
            city = data['city']
            form.fields['city'].queryset = City.objects.filter(pk__exact=city)
        return form


class CatalogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateWithInlinesView):

    model = Catalog
    form_class = CatalogForm
    inlines = [CatalogPhonesFormSet, ]
    success_message = "Catálogo atualizado com sucesso!"

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponse("Unauthorized", 401)
        return super(CatalogUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('catalog:user_list')

    def get_form_kwargs(self):
        kwargs = super(CatalogUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_form(self, form_class=None):
        form = super(CatalogUpdateView, self).get_form(form_class)
        kwargs = self.get_form_kwargs()
        if "data" in kwargs:
            data = kwargs['data'].dict()
            city = data['city']
            form.fields['city'].queryset = City.objects.filter(pk__exact=city)
        return form


class CatalogUserListView(LoginRequiredMixin, generic.ListView):
    """ Listagem dos catálogos no painel do usuário
    """
    model = Catalog
    template_name = "catalog/cataloguser_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super(CatalogUserListView, self).get_queryset()
        queryset = queryset.filter(user__exact=self.request.user.pk)
        return queryset


class CatalogMail(generic.FormView):

    form_class = CatalogEmail
    template_name = "catalog/catalogmail_form.html"

    def get_success_url(self):
        return reverse('catalog:list')

    def get_context_data(self, **kwargs):
        kwargs = super(CatalogMail, self).get_context_data(**kwargs)
        return kwargs

    def get_object(self):
        return Catalog.objects.get(pk=1)  # TODO

    def form_valid(self, form):
        obj = self.get_object()
        url = reverse("catalog:list")
        fullpath = "".join(
            ["http://", get_current_site(self.request).domain, url])
        form.send_mail(obj.email, obj.name, fullpath)
        messages.success(
            self.request,
            _(u"Obrigado! Sua mensagem foi enviada com sucesso!")
        )
        return super(CatalogMail, self).form_valid(form)


class CatalogDetailView(generic.DetailView):

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponse("Unauthorized", 401)
        return super(CatalogDetailView, self).dispatch(request, *args, **kwargs)

    model = Catalog


class CatalogCheckout(generic.DetailView):

    template_name = "catalog/catalog_checkout.html"
    model = Catalog

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user != obj.user:
            return HttpResponse("Unauthorized", 401)

        if obj.is_active == True:
            return HttpResponse("Unauthorized", 401)

        self.request.session['c_checkout'] = obj.pk
        self.request.session.set_expiry(150)

        return super(CatalogCheckout, self).dispatch(request, *args, **kwargs)
