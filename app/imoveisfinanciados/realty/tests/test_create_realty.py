# -*- coding: utf-8 -*-

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import resolve_url as r
from django.test import TestCase, override_settings
from imoveisfinanciados.core.models import State, City
from imoveisfinanciados.realty.forms import RealtyForm


class CreateRealtyGetTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            email='bsbruno1@gmail.com',
            first_name='Bruno',
            last_name='Bruno Barbosa',
            phone='(61) 9999-9999',
            password='123456',
        )
        self.client.login(email='bsbruno1@gmail.com', password='123456')
        self.resp = self.client.get(r('myrealties:add'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'realty/realty_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, RealtyForm)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')


class CreateRealtyPostValid(TestCase):
    def setUp(self):
        state = State.objects.create(
            abbr='DF',
            name='Distrito Federal'
        )
        City.objects.create(
            name='Brasilia',
            state=state,
            max_mcmv=Decimal('10.00'),
            subsidy_max=Decimal('10.00'),
            subsidy_min=Decimal('10.00'),
            multsub=Decimal('1.00')
        )

        get_user_model().objects.create_user(
            email='bsbruno1@gmail.com',
            first_name='Bruno',
            last_name='Bruno Barbosa',
            phone='(61) 9999-9999',
            password='123456',
        )
        self.client.login(email='bsbruno1@gmail.com', password='123456')

        data = dict(
            title='Test realty',
            description='Realty description text',
            type='apt',
            state='1',
            city='1',
            value='1500.00',
            bedroom=2,
            bathroom=1,
            size=64,
            main_image=self.get_image_file(),
        )

        # formset
        data.update({
            'photos-TOTAL_FORMS': '1',
            'photos-INITIAL_FORMS': '0',
            'photos-MIN_NUM_FORMS': '',
            'photos-MAX_NUM_FORMS': '7',
        })
        self.resp = self.client.post(r('myrealties:add'), data)

    def test_post(self):
        self.assertEqual(302, self.resp.status_code)

    def test_redirect(self):
        self.assertRedirects(self.resp, reverse('myrealties:user_realties'))

    @override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
    def get_image_file(self):
        TINY_GIF = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
        from django.core.files.uploadedfile import SimpleUploadedFile
        return SimpleUploadedFile('tiny.gif', TINY_GIF)
