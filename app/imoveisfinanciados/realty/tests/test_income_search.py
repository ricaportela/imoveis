# -*- coding: utf-8 -*-

from urllib.parse import urlencode

from django.urls import reverse
from django.test import TestCase
from imoveisfinanciados.realty.tests.base import RealtyBaseTest
from imoveisfinanciados.simulator.tests.base import SimulatorBaseTest


class IncomeSearchGetValid(SimulatorBaseTest, RealtyBaseTest, TestCase):

    def setUp(self):
        super(IncomeSearchGetValid, self).setUp()
        self.target = reverse('realty:income_search', kwargs={'state': 'br'})
        data = {
            'state': '1',
            'city': '1',
            'birthday': '1989',
            'income': '1.600,00',
        }
        url = '{0}?{1}'.format(self.target, urlencode(data))
        self.resp = self.client.get(url)

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_state_and_city_search_result(self):
        self.assertEqual(1, len(self.resp.context['object_list']))

    def test_simulator_must_exists_on_context(self):
        self.assertIsInstance(self.resp.context['simulator'], dict)
