from __future__ import unicode_literals, absolute_import

import json
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from visitor.models import Visitor

# TODO: CREATE TEST CASES!


# Create your tests here.
class VendorTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.vendor_data = {'weixin': 'weixinweixin'}

    def test_rest_login_success(self):
        """ Test login view for all accounts """
        url = reverse('visitor:login')
        response = self.client.post(url, data=self.vendor_data)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
