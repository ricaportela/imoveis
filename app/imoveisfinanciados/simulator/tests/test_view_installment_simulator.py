# -*- coding: utf-8 -*-

from django.urls import reverse
from django.shortcuts import resolve_url as r
from django.test import TestCase
from imoveisfinanciados.realty.tests.base import RealtyBaseTest
from imoveisfinanciados.simulator.tests.base import SimulatorBaseTest


class InstallmentSimulatorViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('simulators:installment'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'simulator/installment.html')

    def test_template_has_form(self):
        self.assertIn('form', self.resp.context)


class InstallmentSimulatorPostValid(SimulatorBaseTest, RealtyBaseTest, TestCase):

    def setUp(self):
        super(InstallmentSimulatorPostValid, self).setUp()
        data = {
            'state': '1',
            'city': '1',
            'birthday': '1989',
            'installment': '480,00',
        }
        self.resp = self.client.post(reverse('simulators:installment'), data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_simulator_must_exists_on_context(self):
        self.assertIsInstance(self.resp.context['simulator'], dict)

    def test_installment_must_exists_on_context(self):
        self.assertIsInstance(self.resp.context['installment'], dict)
