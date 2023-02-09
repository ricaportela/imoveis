# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
from imoveisfinanciados.core.utils import extract_city_data
from .models import Simulator


class IncomeSimulator(object):

    def __init__(self, city, income, birthday, dependents=False):
        self.city = extract_city_data(city, dependents)
        self.income = income
        self.birthday = birthday

    def _subsidy(self, simulator):
        ms = self.city['subsidy_max']
        ns = self.city['subsidy_min']
        multsub = self.city['multsub']
        dsub = Decimal(ms) - Decimal(ns)
        x = dsub / Decimal(multsub)
        zss = simulator.income_min_sub
        tss = simulator.income_max_sub
        trs = tss + x
        psub = (trs - tss) ** -1
        zsub = (zss - tss) ** -1
        delta = self.income - Decimal(tss)

        if delta <= 0:
            sub = Decimal(ms)

        elif delta * zsub >= 1:
            sub = 0

        else:
            sub = dsub - dsub * delta * psub + Decimal(ns)
            if self.income >= Decimal(trs) and self.income < Decimal(zss):
                sub = Decimal(ns)
        return sub

    def _payments(self):
        current_year = datetime.now().year
        age = current_year - int(self.birthday)
        d_age = age - 50

        if d_age < 0:
            dv = 0

        else:
            dv = d_age * 12 + 4

        npar = 360 - dv
        return npar

    def _sac(self, simulator, subsidy, payments):
        cred = 0
        pk = dict(income=0)

        for ck in simulator.credit.all().values():
            if self.income < ck['income']:
                dd = ck['income'] - pk['income']
                dc = ck['value'] - pk['value']
                ud = self.income - pk['income']
                vc = (ud * dc) / dd
                cred = vc + pk['value']
                break
            pk = ck

        if cred == 0:
            cred = Decimal(123813.82)

        fi = simulator.interest
        li = fi / payments
        amt = cred / payments

        first_payment = cred * fi + amt
        last_payment = cred * li + amt
        funding_value = cred + subsidy
        result = {
            'funding': funding_value,
            'first_payment': first_payment,
            'last_payment': last_payment
        }
        return result

    def _price(self, subsidy):
        # Valor financiavel
        carta_financiamento = self.income * Decimal(54.77)
        if carta_financiamento> Decimal(106000.00):
            carta_financiamento = Decimal(106000.00)
        funding_value = carta_financiamento + subsidy

        # Primeira parcela
        first_payment = self.income * Decimal(0.30)

        # Ultima parcela
        last_payment = self.income * Decimal(0.294)

        result = {
            'funding': funding_value,
            'first_payment': first_payment,
            'last_payment': last_payment
        }
        return result

    def calc(self):
        # Variaveis do simulador
        simulator = Simulator.objects.all().prefetch_related(
            'credit').latest('id')

        # subsidio
        subsidy = self._subsidy(simulator)

        # Numero de parcelas
        payments = self._payments()

        # SAC
        sac = self._sac(
            simulator=simulator,
            subsidy=subsidy,
            payments=payments,
        )

        price = self._price(subsidy)

        result = {}
        result['sac'] = sac
        result['price'] = price
        result['subsidy'] = subsidy
        result['payments'] = payments

        return result
