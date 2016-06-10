from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib.auth import logout, authenticate, login
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from . import serializers, models
from utils import permissions


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    permission_classes = (permissions.IsStoreOwnerOrReadOnly, )

    def get_queryset(self):
        return models.Store.objects.select_related('district__city__state')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.vendor.pk
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


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
    queryset = models.User.objects.\
        select_related('vendor__store__district__city__state')
    permission_classes = (permissions.IsUserOrReadOnly,)


class ProfileListCreateView(UserMixin, generics.ListCreateAPIView):
    """ READ Python MRO """
    serializer_class = serializers.UserCreateSerializer


class ProfileRetrieveUpdateView(UserMixin, generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer


class ProfilePasswordUpdatedView(UserMixin, generics.UpdateAPIView):
    serializer_class = serializers.UserPasswordSerializer


@api_view(['GET'])
@permission_classes(())
def logout_view(request):
    logout(request)
    return Response({'logout': True}, status=200)


@api_view(['POST'])
@permission_classes(())
def login_view(request):
    data = {}
    status = 401
    try:
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        login(request, user)

        data.update({'username': user.username, 'id': user.pk})
        if hasattr(request.user, 'vendor') \
                and hasattr(request.user.vendor, 'store'):
            data.update({'store': request.user.vendor.store.id})
        status = 200
    except KeyError as e:
        # missing parameter
        data.update({'error': _('Missed parameter {}').format(e)})
        status = 400
    except AttributeError:
        # Unauthenticated user
        data.update({'error': _('Invalid combination of username and password')})

    return Response(data, status=status)

