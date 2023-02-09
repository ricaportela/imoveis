from decimal import Decimal

from django.test import TestCase
from imoveisfinanciados.core.models import City, State


class CityModelTest(TestCase):
    def test_create(self):
        state = State.objects.create(
            abbr='DF',
            name='Distrito Federal'
        )
        City.objects.create(
            name='Brasília',
            state=state,
            max_mcmv=Decimal('1600.00'),
            subsidy_max=Decimal('3200.00'),
            subsidy_min=Decimal('1600.00'),
            multsub=Decimal('0.10'),
            slug='brasilia',
        )
        self.assertTrue(City.objects.exists())