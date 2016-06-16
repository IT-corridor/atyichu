from __future__ import unicode_literals, absolute_import

import hashlib
import md5
import time
import unittest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import connection
from rest_framework.test import APITestCase, APIClient

from visitor.models import Visitor

from .models import Mirror, Group, Member, Tag

# TODO: CREATE TEST CASES!
VENDOR = connection.vendor

visitor_data_1 = {"weixin": "oRFOiwzjygVD6hwtyMFUZCZ299bo",
                  "access_token": "ACCESS_TOKEN",
                  "refresh_token": "REFRESH_TOKEN",
                  "expires_in": 7200,
                  "token_date": "2016-06-15T07:08:04.960Z"}

visitor_data_2 = {"weixin": "oRFOiwzjygVD6hwtyMFUZCZ299b1",
                  "access_token": "ACCESS_TOKEN",
                  "refresh_token": "REFRESH_TOKEN",
                  "expires_in": 7200,
                  "token_date": "2016-06-15T07:08:04.960Z"}

# Create your tests here.
class MirrorTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(username='Nikolay')
        user_2 = User.objects.create(username='Jack')

        Visitor.objects.create(user=user_1, **visitor_data_1)
        Visitor.objects.create(user=user_2, **visitor_data_2)

        cls.vendor_data_1 = {'weixin': 'oRFOiwzjygVD6hwtyMFUZCZ299bo'}
        cls.vendor_data_2 = {'weixin': 'oRFOiwzjygVD6hwtyMFUZCZ299b1'}
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

        cls.now = time.time()
        key = "sdlfkj9234kjlnzxcv90123098123asldjk"
        cls.checksum = hashlib.md5('{}{}'.format(key, cls.now)).hexdigest()

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

    @unittest.skip("It works. just skippend")
    def test_mirror_view_detail(self):

        self.force_login()
        Mirror.objects.lock()
        time.sleep(61)
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

        data = {'token': 'Ar3dltB4VSVwaasOfRkJbPojq28Q2dzxC1vZ1TczDQBH',
                'timestamp': self.now,
                'checksum': self.checksum,
        }
        self.force_login()
        response = self.client.post(reverse('snapshot:mirror-status'),
                                    data=data)

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_create_mirror(self):

        data = {'token': 'weixin',
                'latitude': 10,
                'longitude': 10,
                'title': 'iSmarror for e.g.',
                'timestamp': self.now,
                'checksum': self.checksum}
        url = reverse('snapshot:mirror-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def force_login(self):
        user = User.objects.get(id=2)
        self.client.force_login(user=user)


class GroupTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(username="Nikolay")
        cls.owner = Visitor.objects.create(user=user_1, **visitor_data_1)

        user_2 = User.objects.create(username="Jack")
        cls.member = Visitor.objects.create(user=user_2, **visitor_data_2)

        cls.group = Group.objects.create(owner=cls.owner, title='group 0')
        cls.group_private = Group.objects.create(owner=cls.owner, title='G 0',
                                                 is_private=True)
        Member.objects.create(visitor=cls.member, group=cls.group_private)
        Tag.objects.create(title='Primal', visitor=cls.owner, group=cls.group)
        Tag.objects.create(title='Second', visitor=cls.member, group=cls.group_private)

    def test_create_group(self):
        """ Test creating public group """
        data = {'title': 'test group'}
        self.force_login(1)
        url = reverse('snapshot:group-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.client.logout()

    def test_access_group(self):
        """Access to the public group for not authenticated person """
        url = reverse('snapshot:group-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_access_group_private(self):
        """Test access to the private group from not authenticated person.
        Expect 403 Forbidden."""
        url = reverse('snapshot:group-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_access_group_private_member(self):
        """Test access to the private group from member."""
        self.force_login(2)
        url = reverse('snapshot:group-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_delete_group(self):
        """Test delete group as group owner """
        self.force_login(1)
        url = reverse('snapshot:group-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.client.logout()

    def test_delete_group_as_member(self):
        """Test delete group as group member. Expect 403 Forbidden. """
        self.force_login(2)
        url = reverse('snapshot:group-detail', kwargs={'pk': 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_update_put_as_member(self):
        """ Attempt to update whole group. Expect 403 Forbidden."""
        self.force_login(2)
        url = reverse('snapshot:group-detail', kwargs={'pk': 2})
        response = self.client.put(url, data={'title': 'New title'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_update_patch_as_member(self):
        """ Attempt to update group partially.
        Expect 403 for member / collaborator """
        self.force_login(2)
        url = reverse('snapshot:group-detail', kwargs={'pk': 2})
        response = self.client.patch(url, data={'title': 'New title'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_create_tag_for_group(self):
        """ Add tag as group owner """
        self.force_login(1)
        url = reverse('snapshot:tag-list')
        response = self.client.post(url, data={'title': 'new tag', 'group': 2})
        self.assertEqual(response.status_code, 201)
        self.client.logout()

    def test_create_tag_member_for_group(self):
        """ Add tag as group owner """
        self.force_login(2)
        url = reverse('snapshot:tag-list')
        response = self.client.post(url, data={'title': 'new tag2',
                                               'group': 2})
        self.assertEqual(response.status_code, 201)
        self.client.logout()

    def test_update_tag_group(self):
        self.force_login(1)
        url = reverse('snapshot:tag-detail', kwargs={'pk': 1})
        response = self.client.patch(url, data={'title': 'updated'})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_delete_group_tag(self):
        """ Delete tag as group owner """
        self.force_login(1)
        url = reverse('snapshot:tag-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.client.logout()

    def test_update_tag_group_member(self):
        """Expect 403."""
        self.force_login(2)
        url = reverse('snapshot:tag-detail', kwargs={'pk': 1})
        response = self.client.patch(url, data={'title': 'updated'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_delete_tag_group_member(self):
        """ Expect 403 """
        self.force_login(2)
        url = reverse('snapshot:tag-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_delete_tag_group_member_own(self):
        self.force_login(2)
        url = reverse('snapshot:tag-detail', kwargs={'pk': 2})
        response = self.client.delete(url)
        print(response.data)
        self.assertEqual(response.status_code, 204)
        self.client.logout()

    def force_login(self, pk):
        user = User.objects.get(id=pk)
        self.client.force_login(user=user)
