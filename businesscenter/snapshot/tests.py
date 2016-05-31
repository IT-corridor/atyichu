from __future__ import unicode_literals, absolute_import

import json
import unittest
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from django.db import connection

from visitor.models import Visitor

from .models import Mirror, MirrorManager

# TODO: CREATE TEST CASES!

VENDOR = connection.vendor
# Create your tests here.
class MirrorTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.vendor_data_1 = {'weixin': 'oRFOiwzjygVD6hwtyMFUZCZ299bo'}
        cls.vendor_data_2 = {'weixin': 'oRFOiw7WT39SToNkgAIEg87BxqPw'}
        url = reverse('visitor:login')
        client = APIClient()
        response = client.post(url, data=cls.vendor_data_1)
        assert response.status_code == 200
        client.logout()

        response = client.post(url, data=cls.vendor_data_2)
        assert response.status_code == 200
        client.logout()

        cls.visitor_1 = Visitor.objects.get(pk=1)
        cls.visitor_2 = Visitor.objects.get(pk=2)
        cls.data_1 = {'title': 'first mirror', 'location': 'china sanlitun',
                      'is_locked': False, 'latitude': 22.299439,
                      'longitude': 114.173881, 'owner': cls.visitor_1,
                      'token': 'AqVlo9fwZJP66WHQBxsL0qMGq507aHBkO0lC3MS5'}

        cls.data_2 = {'title': 'opplya', 'location': 'beijing',
                      'is_locked': False, 'latitude': 39.929344,
                      'longitude': 116.48178, 'owner': cls.visitor_2,
                      'token': 'Ar3dltB4VSVwaasOfRkJbPojq28Q2dzxC1vZ1TczDQBH'}

        cls.data_3 = {'title': 'opzlya', 'location': 'beijing',
                      'is_locked': False, 'latitude': 39.929344,
                      'longitude': 116.48178, 'owner': cls.visitor_2,
                      'token': 'Ar3dltB4VSVwaasOfRkJbPojq28Q2dzxC1vZ1TczDsBH'}

        cls.mirror_1 = Mirror.objects.create(**cls.data_1)
        cls.mirror_2 = Mirror.objects.create(**cls.data_2)
        cls.mirror_3 = Mirror.objects.create(**cls.data_3)

    def test_mirror_last_login(self):
        self.mirror_1.update_last_login()
        self.assertTrue(self.mirror_1.is_online())

    def test_mirror_locked(self):
        self.mirror_1.lock()
        self.assertTrue(self.mirror_1.is_locked)
        self.assertTrue(self.mirror_1.is_overtime())

    def test_mirrors_locked_then_unlock(self):
        Mirror.objects.all().lock()
        locked = Mirror.objects.all()
        for mirror in locked:
            self.assertTrue(mirror.is_locked)

        Mirror.objects.all().unlock()
        unlocked = Mirror.objects.all()
        for mirror in unlocked:
            self.assertFalse(mirror.is_locked)

    @unittest.skipIf(VENDOR == 'sqlite', 'SQRT not supported')
    def test_nearest_mirrors(self):
        mirrors = Mirror.objects.get_by_distance(39.929344, 116.48178)

        self.assertTrue(len([x for x in mirrors]) == 2)

    def test_mirror_view_unlock(self):
        self.force_login()
        response = self.client.post(reverse('snapshot:mirror-unlock'))

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    @unittest.skipIf(VENDOR == 'sqlite', 'SQRT not supported')
    def test_mirror_view_list(self):
        self.force_login()
        response = self.client.get(reverse('snapshot:mirror-list'))

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_mirror_view_detail(self):
        self.force_login()
        response = self.client.get(reverse('snapshot:mirror-detail',
                                           kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_mirror_view_update(self):
        self.force_login()
        response = self.client.patch(reverse('snapshot:mirror-detail',
                                           kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_mirror_view_status(self):
        # EXPECTED ERROR
        self.force_login()
        response = self.client.post(reverse('snapshot:mirror-status'))

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def force_login(self):
        user = User.objects.get(id=2)
        self.client.force_login(user=user)
