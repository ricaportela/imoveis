from django.urls import path, re_path

from .views import SimulatorsPageView, IncomeSimulatorView, InstallmentSimulatorView

app_name = 'simulator'
urlpatterns = [
    re_path('renda/', IncomeSimulatorView.as_view(), name='income'),
    re_path('prestacao/', InstallmentSimulatorView.as_view(), name='installment'),
    re_path('',
        SimulatorsPageView.as_view(),
        name="list"
        ),
]
