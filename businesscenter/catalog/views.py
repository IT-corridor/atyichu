from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend, \
    OrderingFilter, SearchFilter
from . import serializers, models
from .filters import CommodityFilter
from utils import permissions
from utils.views import OwnerCreateMixin, OwnerUpdateMixin


class ReferenceMixin(OwnerCreateMixin, OwnerUpdateMixin):
    """ Only vendor can see his commodities and references """
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    user_kwd = 'store'

    def get_queryset(self):
        return self.model.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly, )
    serializer_class = serializers.CategorySerializer
    model = models.Category


class KindViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly,)
    serializer_class = serializers.KindSerializer
    model = models.Kind


class SizeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly,)
    serializer_class = serializers.SizeSerializer
    queryset = models.Size.objects.all()


class BrandViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.BrandSerializer
    model = models.Brand


class ColorViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly,)
    serializer_class = serializers.ColorSerializer
    queryset = models.Color.objects.all()


class GalleryViewSet(viewsets.ModelViewSet):
    # TODO: implement permissions
    serializer_class = serializers.GallerySerializer
    queryset = models.Gallery.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class CommodityViewSet(ReferenceMixin, viewsets.ModelViewSet):
    # TODO: Add filter
    model = models.Commodity
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = CommodityFilter
    ordering_fields = ('id', 'title',)
    search_fields = ('title', 'kind__title', 'kind__category__title',
                     'brand__title', 'color__title', 'size__title', 'tag__title')

    def get_queryset(self):
        qs = super(CommodityViewSet, self).get_queryset()
        return qs.select_related('brand', 'kind__category', 'color', 'size').\
            prefetch_related('gallery_set', 'tag_set')

    def get_serializer_class(self):
        if self.request.method == 'GET' or not self.kwargs.get('pk', None):
            return serializers.CommodityListSerializer
        return serializers.CommodityDetailSerializer

    def perform_create(self, serializer):
        """ First of all we creating a new commodity.
        After this we create photos for it. After it we add to five (5) bounded
        photos to gallery table (with help of model)"""
        commodity = serializer.save()
        files = self.request.FILES
        serializer_class = serializers.GallerySerializer
        for n, k in enumerate(files.keys()):
            data = {'commodity': commodity.id, 'photo': files[k]}
            serializer = serializer_class(data=data)
            serializer.is_valid(True)
            serializer.save()
            if n > 4:
                break
