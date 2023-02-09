# -*- coding: utf-8 -*-
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SimulatorsListPageTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('simulators:list'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'simulator/simulators.html')

    def test_js(self):
        required_js = (
            'updatecities.js', 'searchforms.js'
        )
        for js in required_js:
            with self.subTest():
                self.assertContains(self.resp, js)