from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from imoveisfinanciados.core.models import City, State
from imoveisfinanciados.realty.models import Realty


class CityDetailTest(TestCase):
    def setUp(self):
        state = State.objects.create(
            abbr='DF',
            name='Distrito Federal',
        )
        city = City.objects.create(
            name='Brasília',
            state=state,
            max_mcmv=Decimal('1600.00'),
            subsidy_max=Decimal('3200.00'),
            subsidy_min=Decimal('1600.00'),
            multsub=Decimal('0.10'),
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
            title='Test realty',
            description='Realty description text',
            type='apt',
            state=state ,
            city=city,
            value=Decimal('1500.00'),
            bedroom=2,
            bathroom=1,
            size=64,
            main_image=self.get_image_file(),
        )
        self.resp = self.client.get('/df/brasilia/')

    @override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
    def get_image_file(self):
        TINY_GIF = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
        from django.core.files.uploadedfile import SimpleUploadedFile
        return SimpleUploadedFile('tiny.gif', TINY_GIF)

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_context(self):
        self.assertEqual(1, len(self.resp.context['object_list']))