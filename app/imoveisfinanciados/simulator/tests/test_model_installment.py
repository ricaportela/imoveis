# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase
from imoveisfinanciados.simulator.models import InstallmentConstant


class InstallmentModelTest(TestCase):
    def test_create(self):
        InstallmentConstant.objects.create(
            type='sac',
            value=Decimal('0.3')
        )
        self.assertTrue(InstallmentConstant.objects.exists())