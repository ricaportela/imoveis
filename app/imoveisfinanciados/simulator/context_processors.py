# -*- coding: utf-8 -*-

from imoveisfinanciados.realty.forms import AdvancedSearchForm
from imoveisfinanciados.simulator.forms import IncomeSearchForm, InstallmentForm


def search_forms(request):
    initial = {}
    if request.method == "GET":
        data = request.GET.dict()
        if 'csrfmiddlewaretoken' in data:
            data.pop("csrfmiddlewaretoken")
        # if "state" in data:
        #     data.pop("state")
        initial = data

    return {
        'income_form': IncomeSearchForm(initial=initial),
        'advanced_form': AdvancedSearchForm(initial=initial),
        'installment_form': InstallmentForm(initial=initial)
    }