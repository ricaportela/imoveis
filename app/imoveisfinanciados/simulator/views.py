# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.http import QueryDict
from django.views.generic import TemplateView, FormView
from imoveisfinanciados.simulator.forms import IncomeSearchForm, InstallmentForm
from imoveisfinanciados.simulator.incomesimulator import IncomeSimulator
from imoveisfinanciados.simulator.installmentsimulator import InstallmentSimulator
from imoveisfinanciados.utils.money import clean_money


class SimulatorsPageView(TemplateView):
    template_name = 'simulator/simulators.html'


class IncomeSimulatorView(FormView):
    form_class = IncomeSearchForm
    template_name = 'simulator/income.html'
    success_url = reverse_lazy('simulators:income')

    def get_form_kwargs(self):
        kwargs = super(IncomeSimulatorView, self).get_form_kwargs()
        if self.request.method == 'POST':
            data_ = self.request.POST.dict()
            data_['income'] = clean_money(data_['income'])

            qdict = QueryDict('', mutable=True)
            qdict.update(data_)

            kwargs['data'] = qdict

        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        simulator_ = IncomeSimulator(
            data['city'], data['income'], data['birthday'], data['dependents'])
        simulator = simulator_.calc()
        return self.render_to_response(self.get_context_data(simulator=simulator))


class InstallmentSimulatorView(FormView):
    form_class = InstallmentForm
    template_name = 'simulator/installment.html'
    success_url = reverse_lazy('simulators:installment')

    def get_form_kwargs(self):
        kwargs = super(InstallmentSimulatorView, self).get_form_kwargs()
        if self.request.method == 'POST':
            data_ = self.request.POST.dict()
            data_['installment'] = clean_money(data_['installment'])

            qdict = QueryDict('', mutable=True)
            qdict.update(data_)

            kwargs['data'] = qdict

        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        installment_simulator = InstallmentSimulator(data['installment'])
        income = installment_simulator.calc()
        simulator_ = IncomeSimulator(
            data['city'], income['price'], data['birthday'], data['dependents'])
        simulator = simulator_.calc()
        return self.render_to_response(
            self.get_context_data(
                simulator=simulator,
                installment=income,
                searched=data['installment']
            )
        )
