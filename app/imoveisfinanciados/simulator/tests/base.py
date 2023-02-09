# -*- coding: utf-8 -*-
from decimal import Decimal

from imoveisfinanciados.simulator.models import Simulator, Credit, InstallmentConstant


class SimulatorBaseTest(object):
    def setUp(self):
        simulator = Simulator.objects.create(
            interest=Decimal('0.0043'),
            income_max_sub=Decimal('1600.00'),
            income_min_sub=Decimal('3275.00'),
            min_income=Decimal('600.00')
        )

        Credit.objects.create(
            income=Decimal('600.00'),
            value=Decimal('25411.78'),
            simulator=simulator
        )

        Credit.objects.create(
            income=Decimal('2400.00'),
            value=Decimal('101647.12'),
            simulator=simulator
        )

        Credit.objects.create(
            income=Decimal('2500.00'),
            value=Decimal('94537.90'),
            simulator=simulator
        )

        Credit.objects.create(
            income=Decimal('3250.00'),
            value=Decimal('123844.66'),
            simulator=simulator
        )

        InstallmentConstant.objects.create(
            type='sac',
            value=Decimal('0.30')
        )

        InstallmentConstant.objects.create(
            type='price',
            value=Decimal('0.30')
        )

        return super(SimulatorBaseTest, self).setUp()