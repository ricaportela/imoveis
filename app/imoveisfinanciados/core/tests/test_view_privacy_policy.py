from django.test import TestCase


class PrivacyPolicyGetValid(TestCase):
    def test_get(self):
        resp = self.client.get('/politica-de-privacidade/')
        self.assertEqual(200, resp.status_code)