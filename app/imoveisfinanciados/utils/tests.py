# -*- coding: utf-8 -*-

import unittest

from imoveisfinanciados.utils.money import money_format, normalize_money, clean_money


class TestMoneyUtils(unittest.TestCase):
    def test_money_format(self):
        self.assertEqual('R$ 10,00', money_format(10.0))
        self.assertEqual('R$ 10,00', money_format(10))

    def test_normalize_money(self):
        self.assertEqual('10.000', normalize_money('10,000'))

    def test_clean_money(self):
        """clean money must converts 150.000,00 (BRL format) to 150000.00 (Decimal format)"""
        self.assertEqual('150000.00', clean_money('150.000,00'))