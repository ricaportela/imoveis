from django.urls import path, re_path

from .views import *

app_name = 'user_realties'
urlpatterns = [
    re_path('',
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
]
