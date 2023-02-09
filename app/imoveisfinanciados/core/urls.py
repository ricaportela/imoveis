from django.urls import path,re_path

from .views import JsonCitiesList

app_name = 'core'
urlpatterns = [
    re_path('get/cities/(?P<pk>\d+)/',
        JsonCitiesList.as_view(),
        name="city_list"
        ),
]
