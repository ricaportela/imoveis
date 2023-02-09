# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase
from imoveisfinanciados.simulator.installmentsimulator import InstallmentSimulator
from imoveisfinanciados.simulator.models import InstallmentConstant


class InstallmentSimulatorTest(TestCase):
    def setUp(self):
        InstallmentConstant.objects.create(
            type='sac',
            value=Decimal('0.3')
        )
        InstallmentConstant.objects.create(
            type='price',
            value=Decimal('0.3')
        )
        self.simulator = InstallmentSimulator(Decimal('480.00'))
        self.constant_types = ('sac', 'price')

    def test_calc_return_dict(self):
        self.assertIsInstance(self.simulator.calc(), dict)

    def test_get_constants(self):
        for type_ in self.constant_types:
            with self.subTest():
                self.assertIn(type_, self.simulator.get_constants())

    def test_constants_must_be_decimal_type(self):
        constants = self.simulator.get_constants()
        for type_ in self.constant_types:
            with self.subTest():
                self.assertIsInstance(constants[type_], Decimal)

