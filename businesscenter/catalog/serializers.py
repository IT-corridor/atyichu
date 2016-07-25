from __future__ import unicode_literals

from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category


class KindSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Kind


class KindVerboseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

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


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gallery


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag


class CommodityListSerializer(serializers.ModelSerializer):

    # TODO: set parent serializers read-only and add its ids,
    # because of issues with creating/updating)
    tags = TagSerializer(many=True, read_only=True, source='tag_set')
    name = serializers.CharField(source='__unicode__', read_only=True)
    season_text = serializers.CharField(source='get_season_display',
                                        read_only=True)

    cover = serializers.SerializerMethodField(read_only=True)

    def get_cover(self, obj):
        gallery = obj.gallery_set.first()
        if gallery and gallery.thumb.name:
            request = self.context.get('request', None)
            url = gallery.thumb.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return

    class Meta:
        model = models.Commodity


class CommodityDetailSerializer(CommodityListSerializer):
    gallery_set = GallerySerializer(many=True, read_only=True)
    kind = KindVerboseSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
