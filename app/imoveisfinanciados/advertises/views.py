from django.http import JsonResponse
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from imoveisfinanciados.utils.mixin import JSONResponseMixin
from imoveisfinanciados.advertises.models import ADCity, Banner
from imoveisfinanciados.advertises.forms import BannerForm, ADCityForm
from imoveisfinanciados.utils.permissions import PermissionsRequiredMixin


class ADCityListView(PermissionsRequiredMixin, ListView):
    model = ADCity
    paginate_by = 10
    required_permissions = (
        'advertises.change_adcity'
    )


class BannerAjaxCreateView(PermissionsRequiredMixin, SuccessMessageMixin, CreateView):
    model = Banner
    form_class = BannerForm
    success_message = "Banner cadastrado com sucesso!"
    required_permissions = (
        'advertises.add_banner'
    )

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'title': self.object.title
            }
            return JsonResponse(data)
        else:
            return response

    def get_success_url(self):
        return reverse('advertises:banner_detail_json', kwargs={'pk': self.object.pk})


class BannerDetailViewJson(PermissionsRequiredMixin, JSONResponseMixin, DetailView):
    model = Banner
    required_permissions = (
        'advertises.change_banner'
    )

    def options(self, request, *args, **kwargs):
        response = super().options(
            request, *args, **kwargs)
        response['Content-type'] = "application/json"
        return response

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class ADCityCreateView(PermissionsRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ADCityForm
    template_name = 'advertises/adcity_form.html'
    success_message = "Anúncio cadastrado com sucesso!"
    required_permissions = (
        'advertises.add_adcity'
    )

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['banner_form'] = BannerForm
        return kwargs

    def get_success_url(self):
        return reverse('advertises:adcity_list')


# TODO: when open the form, select automatically state and cities saved
class ADCityUpdateView(PermissionsRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ADCity
    form_class = ADCityForm
    template_name = 'advertises/adcity_form.html'
    success_message = "Anúncio atualizado com sucesso!"
    required_permissions = (
        'advertises.add_adcity'
    )

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['banner_form'] = BannerForm
        return kwargs

    def get_success_url(self):
        return reverse('advertises:adcity_list')
