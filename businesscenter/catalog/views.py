from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from rest_framework import viewsets, generics
from . import serializers, models
from rest_framework.response import Response
from utils import permissions

# TODO: Add permissions for the ViewSets


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class KindViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.KindSerializer
    queryset = models.Kind.objects.all()


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()


class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ColorSerializer
    queryset = models.Color.objects.all()


class SizeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SizeSerializer
    queryset = models.Size.objects.all()


class CommodityViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommoditySerializer
    queryset = models.Commodity.objects\
        .select_related('brand', 'kind__category')


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StockSerializer
    queryset = models.Stock.objects.\
        select_related('color', 'size', 'commodity__brand',
                       'commodity__kind__category')


class GalleryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GallerySerializer
    queryset = models.Gallery.objects.all()
