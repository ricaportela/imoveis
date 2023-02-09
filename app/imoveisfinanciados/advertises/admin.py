from imoveisfinanciados.core.models import City, State
from .models import Banner, ADNational, ADCity, ADState
from django.contrib import admin


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title',)


class ADNationalAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'created')
    search_fields = ('title',)


class ADStateAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'created')
    search_fields = ('title',)


class ADCityAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'created')
    search_fields = ('title',)


admin.site.register(Banner, BannerAdmin)
admin.site.register(ADNational, ADNationalAdmin)
admin.site.register(ADCity, ADStateAdmin)
admin.site.register(ADState, ADCityAdmin)
