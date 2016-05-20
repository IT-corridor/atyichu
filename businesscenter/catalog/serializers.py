from __future__ import unicode_literals

from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category


class KindSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Kind


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Brand


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Color


class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Size


class CommoditySerializer(serializers.ModelSerializer):

    # TODO: set parent serializers read-only and add its ids,
    # because of issues with creating/updating
    # TODO: maybe there is will be a reason to merge
    # this serializer and next one and its views. Return here after test cases.

    kind = KindSerializer()
    brand = BrandSerializer()
    name = serializers.CharField(source='__unicode__', read_only=True)
    season_text = serializers.CharField(source='get_season_display',
                                        read_only=True)

    class Meta:
        model = models.Commodity


class StockSerializer(serializers.ModelSerializer):

    commodity = CommoditySerializer()
    name = serializers.CharField(source='__unicode__', read_only=True)

    class Meta:
        model = models.Stock


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gallery

