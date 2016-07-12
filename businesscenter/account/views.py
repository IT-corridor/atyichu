from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib.auth import logout, authenticate, login
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import list_route, detail_route
from rest_framework.generics import get_object_or_404
from . import serializers, models
from .permissions import IsVendorSimple
from utils import permissions
from utils.views import OwnerCreateMixin, OwnerUpdateMixin


class StoreViewSet(OwnerCreateMixin,
                   OwnerUpdateMixin,
                   viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    permission_classes = (permissions.IsStoreOwnerOrReadOnly, )

    # TODO: implement retrieve from session
    def get_queryset(self):
        return models.Store.objects.select_related('district__city__state')

    @list_route(methods=['get'])
    def my_store(self, request):
        vendor = request.user.vendor
        obj = get_object_or_404(self.get_queryset(), owner=vendor)
        serializer = self.serializer_class(instance=obj,
                                           context={'request': request})
        return Response(data=serializer.data)


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

        if hasattr(user, 'vendor'):
            vendor = user.vendor
            serializer = serializers.VendorBriefSerializer(instance=vendor)
            data.update(serializer.data)
            status = 200
            login(request, user)
    except KeyError as e:
        # missing parameter
        data.update({'error': _('Missed parameter {}').format(e)})
        status = 400
    except AttributeError:
        # Unauthenticated user
        data.update({'error': _('Invalid combination of username and password')})

    return Response(data, status=status)


@api_view(['GET'])
@permission_classes((IsVendorSimple,))
def get_my_vendor(request):
    """ Provides personal vendor data, username and thumb """
    # TODO: Optimize queryset
    vendor = request.user.vendor
    serializer = serializers.VendorBriefSerializer(instance=vendor)
    return Response(data=serializer.data)


@api_view(['GET'])
@permission_classes([])
def is_authenticated(request):
    if request.user.is_authenticated() \
            and hasattr(request.user, 'vendor'):
        r = True
    else:
        r = False
    return Response({'is_authenticated': r})
