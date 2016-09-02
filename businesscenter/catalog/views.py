from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import list_route, detail_route
from rest_framework.filters import DjangoFilterBackend, \
    OrderingFilter, SearchFilter
from rest_framework.response import Response

from . import serializers, models
from .filters import CommodityFilter
from .permissions import IsCommodityPhotoOwnerOrReadOnly
from utils import permissions
from utils.views import OwnerCreateMixin, OwnerUpdateMixin
from utils.parsing import parse_json_data


class ReferenceMixin(OwnerCreateMixin, OwnerUpdateMixin):
    """ Only vendor can see his commodities and references """
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    user_kwd = 'store'

    def get_queryset(self):
        return self.model.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly, )
    serializer_class = serializers.CategorySerializer
    pagination_class = None
    queryset = models.Category.objects.all()


class KindViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly,)
    serializer_class = serializers.KindSerializer
    pagination_class = None
    filter_fields = ('category',)
    queryset = models.Kind.objects.all()


class SizeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly,)
    serializer_class = serializers.SizeSerializer
    pagination_class = None
    queryset = models.Size.objects.all()


class BrandViewSet(ReferenceMixin, viewsets.ModelViewSet):
    serializer_class = serializers.BrandSerializer
    pagination_class = None
    model = models.Brand


class ColorViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminOrReadOnly,)
    serializer_class = serializers.ColorSerializer
    pagination_class = None
    queryset = models.Color.objects.all()


class GalleryViewSet(viewsets.ModelViewSet):
    # TODO: implement permissions
    permission_classes = (IsCommodityPhotoOwnerOrReadOnly,)
    serializer_class = serializers.GallerySerializer
    pagination_class = None
    queryset = models.Gallery.objects.select_related('commodity')
    filter_fields = ('commodity',)

    def perform_create(self, serializer):
        """ Here we checking count of photo bound to the commodity."""
        # it is an ID
        commodity = self.request.data['commodity']
        count = models.Gallery.objects.filter(commodity_id=commodity).count()
        if count >= 5:
            raise ValidationError(_('You can`t add more photos.'))
        serializer.save()

    @list_route(methods=['post'])
    def save_many(self, request, *args, **kwargs):
        """ Saving many photo instances. Bulk creation do not trigger a
        'post save' signal, so thumbs will not be created.
        Also it is not a tested handler.
        It need to be tested. Make a sabotage.
        """
        commodity = request.data['commodity']
        files = request.FILES.copy()
        photo_limit = 5
        count = models.Gallery.objects.filter(commodity_id=commodity).count()
        if count >= photo_limit:
            raise ValidationError(_('You can`t add more photos.'))

        response_data = []
        for n, k in enumerate(files.keys()):
            if n > (photo_limit - count):
                break
            data = {'commodity': commodity, 'photo': files[k]}
            serializer = self.serializer_class(data=data)
            serializer.is_valid(True)
            serializer.save()
            response_data.append(serializer.data)
        return Response(response_data, 201)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    pagination_class = None
    queryset = models.Tag.objects.all()


class CommodityViewSet(ReferenceMixin, viewsets.ModelViewSet):
    # TODO: Add filter
    model = models.Commodity
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = CommodityFilter
    ordering_fields = ('id', 'title',)
    search_fields = ('title', 'kind__title', 'kind__category__title',
                     'colors__title', 'sizes__title',
                     'brand__title', 'tag__title')

    def get_queryset(self):
        qs = super(CommodityViewSet, self).get_queryset()
        qs = qs.select_related('brand', 'kind__category',)
        qs = qs.prefetch_related('colors', 'sizes')
        if self.request.method == 'GET' and self.kwargs.get('pk', None):
            qs = qs.prefetch_related('gallery_set', 'tag_set')
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET' and not self.kwargs.get('pk', None):
            return serializers.CommodityListVerboseSerializer
        return serializers.CommodityListSerializer

    @detail_route(methods=['get'])
    def verbose(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.CommodityVerboseSerializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """ First of all we creating a new commodity.
        After this we create photos for it. After it we add to five (5) bounded
        photos to gallery table (with help of model)"""
        commodity = serializer.save()
        files = self.request.FILES.copy()
        files.pop('color_pic', None)
        photo_limit = 5
        for n, k in enumerate(files.keys()):
            if n > photo_limit:
                break
            data = {'commodity': commodity.id, 'photo': files[k]}
            serializer = serializers.GallerySerializer(data=data)
            serializer.is_valid(True)
            serializer.save()

        stock_set = self.request.data.get('stock_set')
        if stock_set:
            if isinstance(stock_set, unicode):
                stock_set = parse_json_data(stock_set)

            for stock_data in stock_set:
                stock_data['commodity'] = commodity.id
                serializer = serializers.StockSerializer(data=stock_data)
                serializer.is_valid(True)
                serializer.save()

    @list_route(methods=['get'])
    def my(self, request, *args, **kwargs):
        """ It is a list of commodities owned by vendor(store).
        ID of the store received from request.user.
        So it will not depend on authentication backend.
        Important: this view do not provide pagination. """

        if not request.query_params.get('q', None):
            raise ValidationError({'error': _('{} parameter is required').
                                  format('"q"')})
        try:
            # request.query_params['q']
            photo = request.query_params['photo']
            queryset = self.get_queryset().filter(Q(store_id=request.user.pk),
                                                  ~Q(link__photo_id=photo))
            queryset = self.filter_queryset(queryset)[:10]

            serializer = serializers.CommodityLinkSerializer(queryset,
                                                             many=True)
        except KeyError as e:
            raise ValidationError({'error': _('{} parameter is required').
                                  format(e.message)})
        return Response(serializer.data)
