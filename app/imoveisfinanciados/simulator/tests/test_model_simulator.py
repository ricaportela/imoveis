from decimal import Decimal

from django.test import TestCase
from imoveisfinanciados.simulator.models import Simulator, Credit
from imoveisfinanciados.simulator.tests.base import SimulatorBaseTest


class SimulatorBaseModelTest(SimulatorBaseTest, TestCase):

    def test_create_simulator(self):
        self.assertTrue(Simulator.objects.exists())

    def test_create_credits(self):
        self.assertEqual(4, Credit.objects.all().count())