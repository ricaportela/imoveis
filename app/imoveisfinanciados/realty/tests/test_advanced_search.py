# -*- coding: utf-8 -*-

from urllib.parse import urlencode

from django.urls import reverse
from django.test import TestCase
from imoveisfinanciados.realty.tests.base import RealtyBaseTest


class AdvancedSearchGetValid(RealtyBaseTest, TestCase):

    def setUp(self):
        self.target = reverse('realty:advanced_search', kwargs={'state': 'br'})
        super(AdvancedSearchGetValid, self).setUp()

    def test_get(self):
        resp = self.client.get(self.target)
        self.assertEqual(200, resp.status_code)

    def test_max_value_search_result(self):
        data = {
            'keyword': '',
            'min_value': '',
            'max_value': '150.000,00',
            'state': '',
            'city': '',
            'type': '',
        }
        target = reverse('realty:advanced_search', kwargs={'state': 'br'})
        url = '{0}?{1}'.format(target, urlencode(data))
        resp = self.client.get(url)
        self.assertEqual(1, len(resp.context['object_list']))

    def test_min_value_search_result(self):
        data = {
            'keyword': '',
            'min_value': '150.000,00',
            'max_value': '',
            'state': '',
            'city': '',
            'type': 'apt',
        }
        target = reverse('realty:advanced_search', kwargs={'state': 'br'})
        url = '{0}?{1}'.format(target, urlencode(data))
        resp = self.client.get(url)
        self.assertEqual(1, len(resp.context['object_list']))

    def test_state_and_city_search_result(self):
        data = {
            'keyword': '',
            'min_value': '',
            'max_value': '',
            'state': '1',
            'city': '1',
            'type': 'apt',
        }
        target = reverse('realty:advanced_search', kwargs={'state': 'br'})
        url = '{0}?{1}'.format(target, urlencode(data))
        resp = self.client.get(url)
        self.assertEqual(1, len(resp.context['object_list']))

    def test_realty_type_search_result(self):
        data = {
            'keyword': '',
            'min_value': '',
            'max_value': '',
            'state': '',
            'city': '',
            'type': 'casa',
        }
        target = reverse('realty:advanced_search', kwargs={'state': 'br'})
        url = '{0}?{1}'.format(target, urlencode(data))
        resp = self.client.get(url)
        self.assertEqual(1, len(resp.context['object_list']))

    def test_keyword_search_result(self):
        data = {
            'keyword': 'lazer',
            'min_value': '',
            'max_value': '',
            'state': '',
            'city': '',
            'type': '',
        }
        target = reverse('realty:advanced_search', kwargs={'state': 'br'})
        url = '{0}?{1}'.format(target, urlencode(data))
        resp = self.client.get(url)
        self.assertEqual(1, len(resp.context['object_list']))
