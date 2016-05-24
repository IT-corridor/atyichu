from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from rest_framework import viewsets, generics
from . import serializers, models
from rest_framework.response import Response
from . import permissions

# TODO: Add permissions for the ViewSets


class ReferenceMixin(object):
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def get_queryset(self):
        return self.model.objects.filter(store=self.request.user.store)


class CategoryViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    model = models.Category


class KindViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.KindSerializer
    model = models.Kind


class BrandViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.BrandSerializer
    model = models.Brand


class ColorViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ColorSerializer
    model = models.Color


class SizeViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.SizeSerializer
    model = models.Size


class CommodityViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CommoditySerializer
    model = models.Commodity

    def get_queryset(self):
        qs = super(CommodityViewSet, self).get_queryset()
        return qs.select_related('brand', 'kind__category')


class StockViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.StockSerializer
    model = models.Stock

    def get_queryset(self):
        qs = super(StockViewSet, self).get_queryset()
        return qs.select_related('color', 'size', 'commodity__brand',
                                 'commodity__kind__category')


class GalleryViewSet(viewsets.ModelViewSet):
    # TODO: implement permissions
    serializer_class = serializers.GallerySerializer
    queryset = models.Gallery.objects.all()
