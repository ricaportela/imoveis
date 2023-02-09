from django.urls import path, re_path

from .views import *

app_name = 'realty'
urlpatterns = [
    re_path('meus-imoveis/',
        UserRealtyListView.as_view(),
        name="user_realties"
        ),
    re_path('cadastrar/',
        RealtyCreateView.as_view(),
        name="add"
        ),
    re_path('atualizar/(?P<pk>\d+)/',
        RealtyUpdateView.as_view(),
        name="update"
        ),
    re_path('visualizar/(?P<slug>[A-Za-z0-9_-]+)/',
        RealtyDetailView.as_view(),
        name="view"
        ),
    re_path('busca-por-renda/',
        RealtyIncomeSearch.as_view(),
        name="income_search"
        ),
    re_path('busca-avancada/',
        RealtyAdvancedSearch.as_view(),
        name="advanced_search"
        ),
    re_path('busca-por-prestacao/',
        InstallmentSearch.as_view(),
        name="installment_search"
        ),
    re_path('user/get/number/(?P<pk>\d+)/',
        UserNumberJson.as_view(), name="realty_get_number_json"),
    re_path('', RealtyListView.as_view(), name="list")
]
