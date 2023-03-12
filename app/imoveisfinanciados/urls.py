# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from imoveisfinanciados.core.views import ContactUsView, HomePageView, CityListView
from imoveisfinanciados.realty.views import CityDetailView
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url="/static/images/favicon.ico", permanent=True)

"""from django.conf import settings
from django.conf.urls.static import static
"""

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    # re_path('', include('favicon.urls')),
    re_path("^favicon\.ico$", favicon_view),
    re_path("admin/", admin.site.urls),
    re_path(
        "accounts/", include("imoveisfinanciados.account.urls", namespace="accounts")
    ),
    re_path("settings/", include("imoveisfinanciados.core.urls", namespace="settings")),
    re_path(
        "catalogo/", include("imoveisfinanciados.catalog.urls", namespace="catalog")
    ),
    re_path(
        "anuncios/",
        include("imoveisfinanciados.advertises.urls", namespace="advertises"),
    ),
    re_path(
        "simuladores/",
        include("imoveisfinanciados.simulator.urls", namespace="simulators"),
    ),
    re_path("fale-conosco/$", ContactUsView.as_view(), name="contact_us"),
    re_path(
        "politica-de-privacidade/$",
        TemplateView.as_view(template_name="core/privacy_policy.html"),
        name="privacy_policy",
    ),
    re_path("(?P<state>[a-z]{2})/$", CityListView.as_view(), name="city_list"),
    re_path(
        "(?P<state>[a-z]{2})?/imoveis/",
        include("imoveisfinanciados.realty.urls", namespace="realty"),
    ),
    re_path(
        "(?P<state>[a-z]{2})/(?P<slug>[-\w]+)/$",
        CityDetailView.as_view(),
        name="city_detail",
    ),
    re_path(
        "meus-imoveis/",
        include("imoveisfinanciados.realty.user_urls", namespace="myrealties"),
    ),
    re_path("^$", HomePageView.as_view(), name="index"),
]


if settings.DEBUG:
    from django.views.static import serve

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        re_path(
            "media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = _("Imóveis Financiados")
admin.site.site_header = _("Painel de Administração - Imóveis Financiados")
