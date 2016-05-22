from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from account.models import Vendor

# TODO: CREATE TEST CASES!
# TODO: CREATE TEST FOR THE STORE


# Create your tests here.
class VendorTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        Group.objects.get_or_create(name='vendors')

        cls.admin_data = {'username': 'niklak', 'password': 'caesaR65'}
        cls.vendor_data = {'username': 'jack', 'password': 'proPer76'}

        cls.admin = User.objects.create_user(is_superuser=True, **cls.admin_data)
        cls.vendor = Vendor.objects.create_user(**cls.vendor_data)

    def test_admin_password(self):
        self.assertTrue(self.admin.check_password(self.admin_data['password']))

    def test_vendor_password(self):
        self.assertTrue(self.vendor.check_password(self.vendor_data['password']))

    def test_rest_login_success(self):
        """ Test login view for all accounts """
        user = self.vendor
        data_compare = {'username': user.username, 'id': user.id}
        url = reverse('account:login')
        response = self.client.post(url, data=self.vendor_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data_compare)

    def test_rest_login_error_400(self):
        """ Test login view for missing parameter """
        response = self.client.post(reverse('account:login'),
                                    data={'username': 'jack'})
        self.assertEqual(response.status_code, 400)

    def test_rest_login_error_401(self):
        """ Test """
        response = self.client.post(reverse('account:login'),
                                    data={'username': 'peter',
                                          'password': '12345'})

        self.assertEqual(response.status_code, 401)

    def test_rest_login_error_405(self):
        """ Test wrong request method for login view  """
        url = reverse('account:login')
        response = self.client.get(url, data=self.vendor_data)
        self.assertEqual(response.status_code, 405)


