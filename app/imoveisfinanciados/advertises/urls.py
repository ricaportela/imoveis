from django.urls import path, re_path
from imoveisfinanciados.advertises.views import (
    ADCityListView,
    ADCityCreateView,
    ADCityUpdateView,
    BannerAjaxCreateView
)

app_name = 'advertises'
urlpatterns = [
    re_path('municipais/',
        ADCityListView.as_view(),
        name="adcity_list"
        ),
    re_path('municipais/adicionar',
        ADCityCreateView.as_view(),
        name="adcity_create"
        ),
    re_path('municipais/editar/(?P<pk>\d+)',
        ADCityUpdateView.as_view(),
        name="adcity_update"
        ),
    re_path('banner/ajax-add',
        BannerAjaxCreateView.as_view(),
        name="banner_create"
        ),
    re_path('banner/(?P<pk>\d+)/json',
        BannerAjaxCreateView.as_view(),
        name="banner_detail_json"
        ),
]
