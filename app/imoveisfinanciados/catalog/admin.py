# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Catalog, CatalogPhone, CatalogType


class CatalogPhoneInline(admin.StackedInline):
    model = CatalogPhone
    extra = 1


class CatalogAdmin(admin.ModelAdmin):
    """ """
    list_display = (
        "name", "state", "city", "user", "is_active"
    )
    search_fields = ("name", "localization", "state", "city")
    list_filter = ("type", "is_active", "state")
    inlines = (CatalogPhoneInline, )


class CatalogTypeAdmin(admin.ModelAdmin):
    """
    """
    list_display = ("type", "price")


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(CatalogType, CatalogTypeAdmin)
