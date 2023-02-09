from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.shortcuts import resolve_url as r
from imoveisfinanciados.account.forms import RegistrationForm


class CreateAccountGetTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('accounts:auth_register'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'account/register.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, RegistrationForm)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')


class CreateAccountPostValidTest(TestCase):
    def setUp(self):
        data = dict(
            email='bsbruno1@gmail.com',
            first_name='Bruno',
            last_name='Bruno Barbosa',
            phone='(61) 9999-9999',
            password='123456',
            password2='123456',
        )
        self.resp = self.client.post(r('accounts:auth_register'), data)

    def test_post(self):
        """valid post must redirects"""
        self.assertEqual(302, self.resp.status_code)

    def test_redirects(self):
        """valid post must redirects to user realties list admin"""
        self.assertRedirects(self.resp, reverse(
            'realty:user_realties', kwargs=dict(state='br')))

    def test_save_user(self):
        """valid post must create an user"""
        self.assertTrue(get_user_model().objects.exists())


class CreateAccountPostInvalidTest(TestCase):
    def setUp(self):
        data = dict(
            email='bsbruno1@gmail.com',
            first_name='Bruno',
            last_name='Bruno Barbosa',
            phone='(61) 9999-9999',
            password='123456',
            password2='',
        )
        self.resp = self.client.post(r('accounts:auth_register'), data)

    def test_post(self):
        """ Invalid post should not redirects """
        self.assertEqual(200, self.resp.status_code)

    def test_doesnt_save_user(self):
        """invalid post should not save user"""
        self.assertFalse(get_user_model().objects.exists())

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)
