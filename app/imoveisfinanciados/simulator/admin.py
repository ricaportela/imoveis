from django.contrib import admin

from .models import Simulator, Credit, InstallmentConstant


class CreditAdmin(admin.ModelAdmin):

    list_display = ('income', 'value')


class SimulatorAdmin(admin.ModelAdmin):

    list_display = ('interest', 'income_max_sub', 'income_min_sub', 'min_income')


class InstallmentConstantAdmin(admin.ModelAdmin):

    list_display = ('type', 'value')

admin.site.register(Simulator, SimulatorAdmin)
admin.site.register(Credit, CreditAdmin)
admin.site.register(InstallmentConstant, InstallmentConstantAdmin)