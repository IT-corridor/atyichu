from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from rest_framework import viewsets, generics
from . import serializers, models
from rest_framework.response import Response
from utils import permissions


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    #permissions = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        return models.Store.objects.select_related('district__city__state')


class AbsListView(generics.ListAPIView):
    pagination_class = None

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(AbsListView, self).get(request, *args, **kwargs)
        else:
            return Response({'detail': _('FORBIDDEN')}, status=403)


class StateView(AbsListView):

    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer


class CityView(AbsListView):

    queryset = models.City.objects.select_related('state')
    serializers = serializers.CitySerializer


class District(AbsListView):

    queryset = models.District.objects.select_related('city__state')
    serializers = serializers.DistrictSerializer


class UserMixin:
    queryset = models.Vendor.objects.select_related\
        ('store__district__city__state')
    permission_classes = (permissions.IsUserOrReadOnly,)


class ProfileListCreateView(UserMixin, generics.ListCreateAPIView):
    """ Python MRO """
    serializer_class = serializers.UserCreateSerializer


class ProfileRetrieveUpdateView(UserMixin, generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer


class ProfilePasswordUpdatedView(UserMixin, generics.UpdateAPIView):
    serializer_class = serializers.UserPasswordSerializer
