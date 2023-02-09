# -*- coding: utf-8 -*-
from django.urls import reverse
from django.test import TestCase
from django.shortcuts import resolve_url as r
from imoveisfinanciados.realty.tests.base import RealtyBaseTest
from imoveisfinanciados.simulator.tests.base import SimulatorBaseTest


class IncomeSimulatorViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('simulators:income'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'simulator/income.html')

    def test_template_has_form(self):
        self.assertIn('form', self.resp.context)


class IncomeSimulatorPostValid(SimulatorBaseTest, RealtyBaseTest, TestCase):

    def setUp(self):
        super(IncomeSimulatorPostValid, self).setUp()
        data = {
            'state': '1',
            'city': '1',
            'birthday': '1989',
            'income': '1.600,00',
        }
        self.resp = self.client.post(reverse('simulators:income'), data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_simulator_must_exists_on_context(self):
        self.assertIsInstance(self.resp.context['simulator'], dict)
