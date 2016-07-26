from __future__ import unicode_literals, absolute_import

import unittest
import json
import os
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APITestCase

from account.models import Vendor, Store, District, City, State

from .models import Category, Kind, Brand, Color, Size, Commodity, Tag
# TEST DATA

CATEGORIES = [
    {'title': 'skirt'},
    {'title': 'bottom'},
    {'title': 'jacket'},
    {'title': 'coat'},
]

KINDS = [
    {'title': 'car coat', 'category_id': 4},
    {'title': 'pants', 'category_id': 2},
    {'title': 'sport suit', 'category_id': 3},
    {'title': 't-shirts', 'category_id': 3},
    {'title': 'business suit', 'category_id': 3},
    {'title': 'long skirt', 'category_id': 1},
    {'title': 'short skirt', 'category_id': 1},
]

BRANDS = [
    {'title': 'cortigiani'},
    {'title': 'armani'},
    {'title': 'adidas'},
]

COLORS = [
    {'title': 'red', 'html': '#FF0000'},
    {'title': 'orange', 'html': '#FFA500'},
    {'title': 'yellow', 'html': '#FFFF00'},
    {'title': 'green', 'html': '#008000'},
]

SIZES = [
    {'title': 'S'},
    {'title': 'M'},
    {'title': 'L'},
    {'title': 'XL'},
    {'title': 'XXL'},
]

COMMODITIES = [
    {
        'title': 'T-Shirt -13-Ad-23-U',
        'year': '2016',
        'kind_id': 3,
        'brand_id': 3,
        'color_id': 1,
        'size_id': 3,
    },
    {
        'title': 'Mini Skirt 113 as-4-B',
        'year': '2016',
        'kind_id': 7,
        'brand_id': 2,
        'color_id': 3,
        'size_id': 1,
    },
]


class CatalogTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.vendor_data_1 = {'username': 'jack', 'password': 'proPer76'}
        cls.vendor_data_2 = {'username': 'john', 'password': 'groNasd12'}
        cls.customer_data = {'username': 'peter', 'password': 'frAnKly12'}
        vendor_1 = User.objects.create_user(**cls.vendor_data_1)
        vendor_2 = User.objects.create_user(**cls.vendor_data_2)
        cls.vendor_1 = Vendor.objects.create(user=vendor_1)
        cls.vendor_2 = Vendor.objects.create(user=vendor_2)
        cls.customer = User.objects.create_user(**cls.customer_data)

        state = State.objects.create(title='Shanghai')
        city = City.objects.create(title='Shanghai', state=state)
        district = District.objects.create(title='Good', city=city)

        cls.store = Store.objects.create(brand_name='EYE', apt='33',
                                         build_name='Checking',
                                         build_no='44', street='Good street',
                                         district=district, vendor=cls.vendor_2)

        Category.objects.bulk_create(
            tuple((Category(**data) for data in CATEGORIES))
        )
        Kind.objects.bulk_create(
            (Kind(**data) for data in KINDS)
        )
        Brand.objects.bulk_create(
            (Brand(store_id=cls.store.pk, **data) for data in BRANDS)
        )
        Color.objects.bulk_create(
            (Color(**data) for data in COLORS)
        )
        Size.objects.bulk_create(
            (Size(**data) for data in SIZES)
        )

        Commodity.objects.bulk_create(
            (Commodity(store_id=cls.store.pk, **data) for data in COMMODITIES)
        )

        Tag.objects.create(commodity_id=1, title='Awesome')

    def test_commodities_list(self):
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])

        url = reverse('catalog:commodity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['results']) == 2)
        self.client.logout()

    @unittest.skip("As users can browse other stores this test useless")
    def test_empty_commodities_list(self):
        self.client.login(username=self.vendor_data_1['username'],
                          password=self.vendor_data_1['password'])

        url = reverse('catalog:commodity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['results']) == 0)
        self.client.logout()

    def test_reference_create(self):
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])

        url = reverse('catalog:size-list')
        response = self.client.post(url, data={'title': 'XXXL'})
        self.assertEqual(response.status_code, 201)
        self.client.logout()

    def test_patch_create(self):
        """ Since only staff can manage size,
            i expect 403 for patch request"""
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])

        url = reverse('catalog:size-detail', kwargs={'pk': 1})
        response = self.client.patch(url, data={'title': 'XXXL'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_delete_create(self):
        """ Since only staff can manage size,
        i expect 403 for delete request"""
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])

        url = reverse('catalog:size-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_exception_other_vendor(self):

        methods = ['post', 'put', 'patch', 'delete']
        for method in methods:
            self.access_reference(method, self.vendor_data_1)
            self.access_reference(method, self.customer_data)

    def access_reference(self, method, user_data):
        self.client.login(username=user_data['username'],
                          password=user_data['password'])
        url = reverse('catalog:size-detail', kwargs={'pk': 1})
        f = getattr(self.client, method)
        response = f(url)
        self.assertTrue(response.status_code in (403, 404, 405))
        self.client.logout()

    def test_commodity_filter(self):
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])

        url = reverse('catalog:commodity-list')
        response = self.client.get(url, data={'category': 3})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_commodity_search(self):
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])

        url = reverse('catalog:commodity-list')
        response = self.client.get(url, data={'search': 'Awesomea'})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_commodity_ordering(self):
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])

        url = reverse('catalog:commodity-list')
        response = self.client.get(url, data={'o': '-id'})
        self.assertEqual(response.data['results'][0]['id'], 2)
        self.client.logout()

    def test_create_commodity_with_photos(self):
        self.client.login(username=self.vendor_data_2['username'],
                          password=self.vendor_data_2['password'])
        url = reverse('catalog:commodity-list')

        data = {
            'title': 'T-Shirt -13-Ad-23-U',
            'year': '2016',
            'kind': 3,
            'brand': 3,
            'color': 1,
            'size': 3,
            'season': 0,
        }
        fpath1 = os.path.join(settings.MEDIA_ROOT, 'image.jpeg')
        fpath2 = os.path.join(settings.MEDIA_ROOT, 'test.jpg')

        with open(fpath1) as fp1, open(fpath2) as fp2:
            data.update({'file_1': fp1, 'file_2': fp2})

            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, 201)