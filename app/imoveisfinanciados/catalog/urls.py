from django.urls import path, re_path

from .views import (
    CatalogChoiceType,
    CatalogListView,
    CatalogCreateView,
    CatalogUpdateView,
    CatalogUserListView,
    CatalogDetailView,
    CatalogMail,
    CatalogCheckout
)

app_name = 'catalog'
urlpatterns = [
    re_path('tipo/',
        CatalogChoiceType.as_view(),
        name="choice_type"
        ),
    re_path('imobiliarias/cadastrar/',
        CatalogCreateView.as_view(ctype="imobiliaria"), name="imobiliaria_add"),
    re_path('imobiliarias/',
        CatalogListView.as_view(catalog_type="imobiliarias"), name="imobiliaria"),
    re_path('correspondentes/cadastrar/',
        CatalogCreateView.as_view(ctype="correspondente"), name="correspondente_add"),
    re_path('correspondentes/',
        CatalogListView.as_view(catalog_type="correspondentes"), name="correspondente"),
    re_path('incorporadoras/cadastrar/',
        CatalogCreateView.as_view(ctype="incorporadora"), name="incorporadora_add"),
    re_path('incorporadoras/',
        CatalogListView.as_view(catalog_type="incorporadoras"), name="incorporadora"),
    re_path('atualizar/(?P<pk>\d+)/', CatalogUpdateView.as_view(), name="update"),
    re_path('listar/', CatalogUserListView.as_view(), name="user_list"),
    re_path('detalhes/(?P<pk>\d+)', CatalogDetailView.as_view(), name="detail"),

    re_path('get/form/(?P<pk>\d+)/', CatalogMail.as_view(), name="contact_form"),
    re_path('checkout/(?P<pk>\d+)', CatalogCheckout.as_view(), name="checkout"),
    re_path('', CatalogListView.as_view(catalog_type="imobiliarias"), name="list")
]
