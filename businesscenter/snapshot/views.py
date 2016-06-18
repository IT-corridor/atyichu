from __future__ import unicode_literals

import json
import logging
import pickle
import os
from urlparse import urldefrag
from datetime import timedelta
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.mail import mail_admins
from django.db.models import F, Prefetch
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Mirror, Photo, Comment, Tag, Member, Group

from . import serializers
from .permissions import IsOwnerOrMember, MemberCanServe
from .sutils import check_sign
from utils.views import OwnerCreateMixin, OwnerUpdateMixin, VisitorCreateMixin
from visitor.permissions import IsVisitor
from visitor.models import Visitor
from vutils.umeng_push import push_unicast
from vutils.wzhifuSDK import JsApi_pub


log = logging.getLogger(__name__)

# API VIEWSETS


class MirrorViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.MirrorSerializer
    permission_classes = [IsVisitor]

    def get_queryset(self):
        visitor = self.request.user.visitor
        return Mirror.objects.filter(owner=visitor, is_locked=True)

    @list_route(methods=['post'])
    def unlock(self, request, *args, **kwargs):
        """
        unlock the mirror

        omit_serializer: true
        omit_parameters:
            - form

        parameters:
            - name: mirror_id
              paramType: query

        """
        mirrors = self.get_queryset()
        if not mirrors:
            log.info('User {} has not locked devices '.format(request.user))
        else:
            # release all lock mirror of the user
            mirrors.unlock()
        return Response(status=200)

    def list(self, request):
        """
        get the most near mirrors
        ---
        # YAML (must be separated by `---`)

        parameters:
            - name: latitude
              paramType: query
            - name: longitude
              paramType: query
        """
        # todo real latitude longitude
        latitude = request.query_params.get('latitude', 0)
        longitude = request.query_params.get('longitude', 0)
        mirrors = Mirror.objects.get_by_distance(latitude, longitude)

        # TODO: optimize with db query!
        #online_mirrors = [i for i in mirrors if i.is_online()]
        #online_mirrors = [i for i in mirrors]

        # Mirror available if it is not locked or owner is current_user
        # Also mirror should be online.
        visitor = self.request.user.visitor
        a_mirrors = [i for i in mirrors if not i.is_locked or
                     i.owner_id == visitor.pk]
        # TODO remove next line
        serializer = serializers.MirrorSerializer(instance=a_mirrors, many=True)
        return Response(data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        lock mirror
        ---
        # YAML (must be separated by `---`)

        omit_serializer: true
        omit_parameters:
            - form
        """
        # THIS BLOCK TAKES NO SENSE HERE!!!
        mirrors = self.get_queryset()
        if not mirrors:
            # release all lock mirror of the user
            log.info('User {} has not locked devices '.format(request.user))
        else:
            mirrors.unlock()

        pk = kwargs.get('pk', None)
        if not pk:
            return Response(data={'error': _('Mirror id required')},
                            status=400)

        # LOOKS LIKE PRETTY PRETTY STUPID
        try:
            mirror = Mirror.objects.get(id=pk)

        except Mirror.DoesNotExist:
            log.warn('user provide mirror id is not existed')
            return Response(data={'error': _('Mirror does not exists')},
                            status=400)
        # mirror is  unlock  or the lock time is expired 1 minutes
        # todo if the mirror is offline return error
        if mirror.is_overtime():
            return Response(data={'error': _('Mirror is already locked')},
                            status=400)
        mirror.lock()
        # IT WILL REWRITE OWNER IF DIFFERENT PEOPLE USING MIRROR
        mirror.user = request.user
        mirror.save()
        serializer = serializers.MirrorSerializer(mirror)
        return Response(data=serializer.data, status=200)

    def retrieve(self, request, *args, **kwargs):
        """
        query a mirror is online
        ---
        omit_serializer: true
        omit_parameters:
            - form
        # THERE NEED TO PASS A PK PARAM!
        """
        status = 400
        pk = kwargs.get('pk', None)
        try:
            mirror = self.get_queryset().get(id=pk)
            if not mirror.is_online():
                data = {'error': _('Mirror is offline')}
            elif mirror.is_overtime():
                data = {'error': _('Mirror is unavailable')}
            else:
                serializer = serializers.MirrorSerializer(mirror)
                data = serializer.data
                status = 200
        except Mirror.DoesNotExist:
            data = {'error': _('Mirror not available')}

        return Response(data=data, status=status)

    @list_route(methods=['post'])
    def status(self, request, *args, **kwargs):
        """
        THIS REQUEST CALLED FROM ANDROID APP.
        Set a mirror online status.
        ---

        omit_serializer: true
        omit_parameters:
            - form
        parameters:
            - name: timestamp
              paramType: query
            - name: token
              paramType: query
            - name: checksum
              paramType: query

        """
        timestamp = request.data.get('timestamp', None)
        checksum = request.data.get('checksum', None)
        token = request.data.get('token', None)

        if not check_sign(timestamp, checksum):
            return Response(data={'error': _('Checksum error')}, status=400)
        log.info('sign correct')

        if not token:
            return Response(data={'error': _('Token is required')}, status=400)
        try:
            mirror = Mirror.objects.get(token=token)
        except Mirror.DoesNotExist:
            return Response(data={'error': _('Mirror token does not exist')})
        mirror.update_last_login()
        return Response(data={'status': True})

    def create(self, request, *args, **kwargs):
        """
        This request must be received only from android.
        It uses POST method.
        REQUEST PARAMS:
            check:
                checksum --- same as status request has. REQUIRED.
                timestamp --- same as status request has. REQUIRED.
            iSmarror data:
                token --- device token. REQUIRED.
                latitude --- latitude of the device. REQUIRED.
                longitude --- longitude of the device. REQUIRED.
                title --- title (name of device) --- NOT REQUIRED.
        If request is successful response will something like that:
            {u'title': u'iSmarror for e.g.', u'is_locked': False,
             u'longitude': u'10.0000000000',
             u'last_login': u'2016-06-13T10:02:14.011418Z',
             u'is_online': True, u'latitude': u'10.0000000000', u'id': 4}
        Response status in successful case is 201.
        In case of any error server will return 400 status and
        error description.
        An example of request:
        curl curl -H "Content-Type: application/json" -X \
        POST -d '{"checksum":"hexdigest_data_here","timestamp":"time", \
        "token": "mirror_token", "latitude": "10.23", "longitude": "10.23"}' \
        http://atyichu.cn/api/v1/mirror/
        But now we serving on atyichu.com. Keep in mind.
        """

        timestamp = request.data.pop('timestamp', None)
        checksum = request.data.pop('checksum', None)

        if not check_sign(timestamp, checksum):
            return Response(data={'error': _('Checksum error')}, status=400)

        serializer = serializers.MirrorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoDetailSerializer
    permission_classes = [IsVisitor]

    # TODO: test delete
    # TODO: TEST retrieve somehow
    # TODO: maybe it is necessary to turn off pagination

    def create(self, request, *args, **kwargs):
        """
        Creates a primary photo record without actual photo.
        Photo will be provided (as update) through android app.
        ---
        # YAML (must be separated by `---`)

        omit_serializer: true
        omit_parameters:
            - form
        """
        try:
            mirror = Mirror.objects.filter(user=request.user, is_lock=True)[0]
        except IndexError:
            return Response(data={'error': _('The mirror is unlocked')},
                            status=400)

        if not mirror.is_overtime():
            return Response(data={'error': _('The mirror is overtime')},
                            status=400)
        if not mirror.is_online():
            return Response(data={'error': _('Mirror is offline')},
                            status=400)

        if (mirror.lock_date != mirror.modify_date) and\
                (timezone.now() < (mirror.modify_date + timedelta(seconds=2))):
            return Response(data={'error': _('You have to wait for 2 seconds')})

        mirror.is_locked = True
        mirror.user = request.user
        mirror.save()

        visitor = request.user.visitor
        photo = Photo.objects.create(visitor=visitor, mirror=mirror)

        log.info('create photo id: {}'.format(photo.id))
        content = {'photo_id': photo.id}
        # SENDING A request to umeng push service,
        # which will push the ANDROID APP.
        send_json, receive_info = push_unicast('571459b267e58e826f000239',
                                               'ydcfc8leufv2efcm4slwmhb2pfffaiop',
                                               mirror.token, json.dumps(content))

        log.info('umeng json: {}, {}'.format(send_json, receive_info))
        return Response(data={'id': photo.id}, status=201)

    def list(self, request, *args, **kwargs):
        """
        get all photo order by time desc
        """
        visitor = request.user.visitor
        photos = Photo.objects.filter(visitor=visitor).\
            prefetch_related('comment_set__author')

        ser = serializers.PhotoListSerializer(instance=photos,many=True,
                                              context={'request': request})
        return Response(data=ser.data)

    def partial_update(self, request, *args, **kwargs):
        """
        THIS REQUEST CALLED FROM ANDROID APP.
        Upload pictures url parameters plus time parameters also sign
        == + key time field value of md5 value.
        ---
        # YAML (must be separated by `---`)

        omit_serializer: true
        omit_parameters:
            - form
        parameters:
            - name: picture
              type: file
            - name: timestamp
              paramType: query
            #- name: id
            #  paramType: query
        """
        timestamp = request.data.get('timestamp', None)
        checksum = request.data.get('checksum', None)
        if not check_sign(timestamp, checksum):
            return Response(data={'error': _('Checksum error')})
        log.info('sign correct')
        pid = kwargs.get('pk', None)
        if not pid:
            return Response(data={'error': _('Missed argument  - pk')})

        # CLEAR THIS
        try:
            photo = Photo.objects.get(id=pid)
        except Photo.DoesNotExist:
            return Response(data={'error': _('Photo does not exist')})

        serializer = self.serializer_class(instance=photo, data=request.data,
                                           partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @detail_route(methods=['patch'])
    def edit(self, request, *args, **kwargs):
        """ Manual update photo """
        # TODO: SET object permissions
        pid = kwargs.get('pk', None)
        try:
            photo = Photo.objects.get(id=pid)
        except Photo.DoesNotExist:
            return Response(data={'error': _('Photo does not exist')})

        visitor = request.user.visitor

        if visitor.pk != photo.visitor_id:
            return Response(data={'error': _('Only the owner can edit photo')})

        serializer = self.serializer_class(instance=photo, data=request.data,
                                           partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author')
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsVisitor]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['author'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class TagViewSet(mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    # TODO: create actual permissions
    queryset = Tag.objects.select_related('group__owner', 'visitor')
    serializer_class = serializers.TagSerializer
    pagination_class = None
    permission_classes = [MemberCanServe]


class MemberViewSet(viewsets.ModelViewSet):
    """ Useless currently """
    queryset = Member.objects.select_related('group', 'visitor')
    serializer_class = serializers.MemberSerializer
    pagination_class = None
    permission_classes = []


class GroupViewSet(OwnerCreateMixin, viewsets.ModelViewSet):
    # TODO: implement cloning photo to the groups
    permission_classes = [IsOwnerOrMember]
    # For update use only method patch

    def get_queryset(self):
        qs = Group.objects.select_related('owner').prefetch_related('tag_set')
        if self.request.method == 'GET' and not self.kwargs.get('pk', None):
            # TODO: Cannot filter a query once a slice has been taken.
            # TODO: find another way
            prefetch = Prefetch('photo_set',
                                queryset=Photo.objects.all())
            qs = qs.prefetch_related(prefetch)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET' and not self.kwargs.get('pk', None):
            return serializers.GroupListSerializer
        return serializers.GroupDetailSerializer

    @detail_route(methods=['post'])
    def photo_create(self, request, *args, **kwargs):
        """ Handler to save an uploaded photo to the 'group'.
         It is necessary to perform self.get_object to check permission. """

        data = request.data
        data['group'] = self.get_object().id
        data['visitor'] = self.request.user.visitor

        serializer = serializers.PhotoDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)

    @detail_route(methods=['get'])
    def photo_list(self, request, *args, **kwargs):
        group = self.get_object()
        queryset = Photo.objects.filter(group=group)
        serializer_class = serializers.PhotoListSerializer
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def snapshot(self, request, *args, **kwargs):
        """ Handler to save a photo taken from weixin JS API """
        raise NotImplementedError

    @detail_route(methods=['post'])
    def member_add(self, request, *args, **kwargs):
        """ Add visitor to the group by username.
         It is necessary to perform self.get_object to check permission. """
        pk = self.get_object().id
        status = 400
        try:
            username = request.data['username']
            visitor = Visitor.objects.get(user__username=username)
        except KeyError as e:
            data = {e.message: _('This parameter is required')}
        except Visitor.DoesNotExist:
            data = {'error': _('Matching user does not exists')}
        else:
            member_data = {'visitor': visitor, 'group': pk}
            serializer = serializers.MemberSerializer(data=member_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            status = 201
        return Response(data, status=status)

    @detail_route(methods=['delete'])
    def member_remove(self, request, *args, **kwargs):
        """ Remove member from group."""
        status = 400
        try:
            member_id = request.data['member']
            member = Member.objects.get(id=member_id, group=self.get_object())
        except KeyError as e:
            data = {e.message: _('This parameter is required')}
        except Member.DoesNotExist:
            data = {'error': _('Matching collaborator does not exists')}
        else:
            member.delete()
            data = None
            status = 204
        return Response(data, status=status)

    def member_email(self, request, *args, **kwargs):
        """ Invite visitor to the group by email """
        raise NotImplementedError

    def member_invite(self, request, *args, **kwargs):
        """ Add (handle) visitor`s invite to the group """
        raise NotImplementedError

    @detail_route(methods=['post'])
    def tag_create(self, request, *args, **kwargs):
        """ Add a group tag. It is here because of object permissions.
            It is necessary to perform self.get_object to check permission. """
        data = request.data
        data['group'] = self.get_object().id
        data['visitor'] = self.request.user.visitor

        serializer = serializers.TagSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)


class GroupPhotoViewSet(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Photo.objects.select_related('group', 'visitor')
    serializer_class = serializers.PhotoDetailSerializer
    pagination_class = None
    permission_classes = [MemberCanServe]


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_signature(request):
    """ Previously it was mirror and photos views pages. Now it is API. """
    # TODO: replace file serving with redis
    # HOOK for ANGULARJS APP for wxlib purpose
    location = request.query_params.get('location', None)

    if not location:
        return Response(status=400)

    jsapi = JsApi_pub()
    filename = '/tmp/mirrors_weixin_status'
    data = None
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = pickle.load(f)
    if data and data['time'] + timedelta(seconds=7200) >= timezone.now():
        ticket = data['ticket']
    else:
        client_access_token_info = json.loads(jsapi.get_access_tocken())
        client_access_token = client_access_token_info['access_token']
        ticket_info = jsapi.get_jsapi_ticket(client_access_token)
        ticket = json.loads(ticket_info)['ticket']

        with open(filename, 'w+') as f:
            ticket_info = {'ticket': ticket, 'time': timezone.now()}
            f.truncate()
            pickle.dump(ticket_info, f)

    url, frag = urldefrag(location)

    js_info = jsapi.get_signature(url=url, ticket=ticket)
    return Response(data=js_info)


def index(request):
    """ A simple view, which presents only a starting template.
     It is an entry. Later should be migrate to static service like Nginx."""
    return render(request, 'index.html')
