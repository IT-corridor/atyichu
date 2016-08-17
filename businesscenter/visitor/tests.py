from __future__ import unicode_literals, absolute_import

import json
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from visitor.models import Visitor, VisitorExtra, Weixin

# TODO: CREATE TEST CASES!


# Create your tests here.
class VendorTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {"openid": "oRFOiwzjygVD6hwtyMFUZCZ299bo",
                    "access_token": "ACCESS_TOKEN",
                    "refresh_token": "REFRESH_TOKEN",
                    "expires_in": 7200,
                    "token_date": "2016-06-15T07:08:04.960Z"}
        user = get_user_model().objects.create(username="Nikolay")
        visitor = Visitor.objects.create(user=user)
        weixin = Weixin.objects.create(visitor=visitor,
                                        unionid="123")
        VisitorExtra.objects.create(visitor=visitor, weixin=weixin, **cls.data)

    def test_rest_login_success(self):
        """ Test login view for all accounts """
        url = reverse('visitor:login')
        response = self.client.post(url, data={'weixin': self.data['openid']})
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_me(self):
        """ Test retreiving own weixin data """
        user = get_user_model().objects.first()
        self.client.force_login(user=user)
        url = reverse('visitor:me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()



