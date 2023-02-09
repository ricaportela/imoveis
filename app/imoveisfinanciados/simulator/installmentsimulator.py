# -*- coding: utf-8 -*-
from imoveisfinanciados.simulator.models import InstallmentConstant


class InstallmentSimulator(object):
    def __init__(self, installment):
        self.installment = installment

    def calc(self):
        result = dict()
        constants = self.get_constants()
        for k, v in constants.items():
            result[k] = self.installment / v
        return result

    def get_constants(self):
        result = dict()
        constants = InstallmentConstant.objects.all()
        for constant in constants:
            result[constant.type] = constant.value
        return result