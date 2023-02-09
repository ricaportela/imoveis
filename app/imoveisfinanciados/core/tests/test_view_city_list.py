from decimal import Decimal

from django.test import TestCase
from imoveisfinanciados.core.models import State, City


class CityListView(TestCase):
    def setUp(self):
        state = State.objects.create(
            abbr='DF',
            name='Distrito Federal',
        )
        City.objects.create(
            name='Brasília',
            state=state,
            max_mcmv=Decimal('1600.00'),
            subsidy_max=Decimal('3200.00'),
            subsidy_min=Decimal('1600.00'),
            multsub=Decimal('0.10'),
        )
        City.objects.create(
            name='Águas Claras',
            state=state,
            max_mcmv=Decimal('1600.00'),
            subsidy_max=Decimal('3200.00'),
            subsidy_min=Decimal('1600.00'),
            multsub=Decimal('0.10'),
        )

        state2 = State.objects.create(
            abbr='GO',
            name='Goiás',
        )
        City.objects.create(
            name='Águas Lindas',
            state=state2,
            max_mcmv=Decimal('1600.00'),
            subsidy_max=Decimal('3200.00'),
            subsidy_min=Decimal('1600.00'),
            multsub=Decimal('0.10'),
        )
        self.resp = self.client.get('/df/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_context(self):
        """list must return only state filtered cities"""
        self.assertEqual(2, len(self.resp.context['object_list']))

    def test_state_in_context(self):
        """context must have a state name"""
        self.assertEqual('Distrito Federal', self.resp.context['state'].name)