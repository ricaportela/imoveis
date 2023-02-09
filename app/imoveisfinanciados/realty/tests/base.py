from decimal import Decimal
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from imoveisfinanciados.core.models import State, City
from imoveisfinanciados.realty.models import Realty


class RealtyBaseTest(object):

    def setUp(self):
        state = State.objects.create(
            abbr='DF',
            name='Distrito Federal'
        )
        state2 = State.objects.create(
            abbr='GO',
            name='Goiás'
        )
        city = City.objects.create(
            name='Brasilia',
            state=state,
            max_mcmv=Decimal('10.00'),
            subsidy_max=Decimal('10.00'),
            subsidy_min=Decimal('10.00'),
            multsub=Decimal('1.00')
        )
        city2 = City.objects.create(
            name='Goiânia',
            state=state2,
            max_mcmv=Decimal('10.00'),
            subsidy_max=Decimal('10.00'),
            subsidy_min=Decimal('10.00'),
            multsub=Decimal('1.00')
        )
        user = get_user_model().objects.create_user(
            email='bsbruno1@gmail.com',
            first_name='Bruno',
            last_name='Bruno Barbosa',
            phone='(61) 9999-9999',
            password='123456',
        )
        Realty.objects.create(
            user=user,
            title='Imóvel teste 1',
            type='apt',
            state=state,
            city=city,
            value=Decimal('160000.00'),
            bedroom=2,
            bathroom=1,
            size=64,
            main_image=self.get_image_file()
        )
        Realty.objects.create(
            user=user,
            title='Imóvel teste 2 lazer completo',
            type='casa',
            state=state2,
            city=city2,
            value=Decimal('140000.00'),
            bedroom=2,
            bathroom=1,
            size=64,
            main_image=self.get_image_file()
        )
        return super(RealtyBaseTest, self).setUp()

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)