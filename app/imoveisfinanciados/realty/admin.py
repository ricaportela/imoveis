# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Realty, Photo


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1


class RealtyAdmin(admin.ModelAdmin):
    """ """
    list_display = (
        "title", "user", "type", "state",
        "city", "bedroom", "bathroom"
    )
    search_fields = ("title", )
    list_filter = ("type", "state", "bedroom", "bathroom")
    inlines = (PhotoInline, )


class PhotoAdmin(admin.ModelAdmin):
    """ """
    list_display = ("title", "realty")
    search_fields = ("title", "realty__title")


admin.site.register(Realty, RealtyAdmin)
admin.site.register(Photo, PhotoAdmin)
