# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import State, City


class StateAdmin(admin.ModelAdmin):
    """ """
    list_display = ("abbr", "name")


class CityAdmin(admin.ModelAdmin):
    """ """
    list_display = ("name", "state")
    list_filter = ("state", )
    search_fields = ('name', )


admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
