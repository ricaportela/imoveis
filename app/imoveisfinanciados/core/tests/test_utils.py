from decimal import Decimal
from django.test import TestCase
from imoveisfinanciados.core.models import City, State
from imoveisfinanciados.core.utils import extract_city_data
from model_mommy import mommy


class ExtractCityDataTest(TestCase):
    def test_happy_path(self):
        state = mommy.make(State, name='Distrito Federal')
        city = City.objects.create(
            name="Brasília",
            state=state,
            subsidy_max=Decimal('10.00'),
            subsidy_min=Decimal('5.00'),
            multsub=Decimal('7'),
        )
        data = extract_city_data(city)
        self.assertEqual(data['subsidy_max'], city.subsidy_max)
        self.assertEqual(data['subsidy_min'], city.subsidy_min)
        self.assertEqual(data['multsub'], city.multsub)

    def test_happy_path_with_dependents(self):
        state = mommy.make(State, name='Distrito Federal')
        city = City.objects.create(
            name="Brasília",
            state=state,
            d_subsidy_max=Decimal('10.00'),
            d_subsidy_min=Decimal('5.00'),
            d_multsub=Decimal('7'),
        )
        data = extract_city_data(city, dependents=True)
        self.assertEqual(data['subsidy_max'], city.d_subsidy_max)
        self.assertEqual(data['subsidy_min'], city.d_subsidy_min)
        self.assertEqual(data['multsub'], city.d_multsub)

    def test_happy_path_with_null_dependents(self):
        state = mommy.make(State, name='Distrito Federal')
        city = City.objects.create(
            name="Brasília",
            state=state,
            subsidy_max=Decimal('10.00'),
            subsidy_min=Decimal('5.00'),
            multsub=Decimal('7'),
        )
        data = extract_city_data(city, dependents=True)
        self.assertEqual(data['subsidy_max'], city.subsidy_max)
        self.assertEqual(data['subsidy_min'], city.subsidy_min)
        self.assertEqual(data['multsub'], city.multsub)