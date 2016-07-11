from __future__ import unicode_literals

import json
import logging
import pickle
import os
from urlparse import urldefrag
from datetime import timedelta
from django.db import IntegrityError
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.mail import mail_admins
from django.db.models import F, Prefetch, Q, Count
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from .models import Mirror, Photo, Comment, Tag, Member, Group, Like

from . import serializers
from .permissions import IsOwnerOrMember, MemberCanServe, \
    IsPhotoOwnerOrReadOnly
from .sutils import check_sign
from utils.views import OwnerCreateMixin, OwnerUpdateMixin, VisitorCreateMixin
from utils.paginators import CustomPagination
from visitor.permissions import IsVisitor
from visitor.serializers import VisitorShortSerializer
from visitor.models import Visitor
from account.models import Vendor, Store
from account.serializers import VendorStoreSerializer
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
        visitor = self.request.user
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
    model = Photo
    serializer_class = serializers.PhotoDetailSerializer
    permission_classes = [IsPhotoOwnerOrReadOnly]

    # TODO: test delete
    # TODO: TEST retrieve somehow
    # TODO: maybe it is necessary to turn off pagination

    def get_queryset(self):
        qs = Photo.p_objects.select_related('original',
                                            'visitor__visitor')
        p = Prefetch('comment_set',
                     Comment.objects.select_related('author__visitor'))
        qs = qs.prefetch_related(p)
        return qs

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

        visitor = request.user
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
        get all photo order by time desc. Currently not used.
        """
        visitor = request.user
        qs = self.get_queryset()
        qs = qs.prefetch_related('comment_set__author').filter(visitor=visitor)
        photos = qs
        ser = serializers.PhotoListSerializer(instance=photos, many=True,
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

        serializer = serializers.PhotoSerializer(instance=photo,
                                                 data=request.data,
                                                 partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.photo and instance.photo.name:
            instance.group = None
            instance.save()
        else:
            instance.delete()
        return Response(status=204)

    @detail_route(methods=['patch'])
    def edit(self, request, *args, **kwargs):
        """ Manual update photo """
        # TODO: SET object permissions
        pid = kwargs.get('pk', None)
        try:
            photo = Photo.objects.get(id=pid)
        except Photo.DoesNotExist:
            return Response(data={'error': _('Photo does not exist')})

        visitor = request.user

        if visitor.pk != photo.visitor_id:
            return Response(data={'error': _('Only the owner can edit photo')})

        serializer = serializers.PhotoSerializer(instance=photo,
                                                 data=request.data,
                                                 partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @detail_route(methods=['get'])
    def like(self, request, *args, **kwargs):
        """ Handler that increments likes """
        obj = self.get_object()

        try:
            Like.objects.create(visitor_id=request.user.id, photo_id=obj.id)

            # Not using default object or queryset, to reduce the queryset
            like_count = Photo.objects.get(id=obj.id).like_set.count()
            data = {'like_count': like_count}
            status = 200
        except IntegrityError:
            data = {'error': _('You have like it already!')}
            status = 400

        return Response(data, status)

    @list_route(methods=['get'])
    def newest(self, request, *args, **kwargs):
        """ Providing a newest list of public groups photos """
        qs = Photo.a_objects.select_related('original', 'visitor__visitor')
        qs = qs.filter(Q(group__is_private=False) &
                       ~Q(visitor_id=request.user.id))\
            .order_by('-pk').distinct()

        return self.get_list_response(qs, serializers.PhotoListSerializer)

    @detail_route(methods=['post'])
    def clone(self, request, *args, **kwargs):
        """ Make a duplicate from existing photo record. GroupID required."""
        if 'group' not in request.data:
            raise ValidationError({'group': _('This parameter is required.')})

        obj = self.get_object()

        if obj.creator and obj.original:
            creator = obj.creator_id
            original = obj.original_id
        else:
            creator = obj.visitor_id
            original = obj.id

        title = obj.title if not request.data.get('title')\
            else request.data['title']

        description = obj.description if not request.data.get('description') \
            else request.data['description']

        data = {'original': original,
                'creator': creator,
                'visitor': request.user.pk,
                'group': request.data['group'],
                'title': title,
                'description': description}

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    @list_route(methods=['get'])
    def liked_list(self, request, *args, **kwargs):
        """ Providing a photo list of liked photos """
        qs = Photo.p_objects.select_related('original', 'visitor__visitor')
        qs = qs.filter(like__visitor_id=request.user.id)

        return self.get_list_response(qs, serializers.PhotoListSerializer)

    def get_list_response(self, queryset, serializer_class):
        """ Shortcut for the paginated views / handlers """
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author__visitor')
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

    @detail_route(methods=['get'])
    def like(self, request, *args, **kwargs):
        """ Handler that increments likes """
        obj = self.get_object()
        status = 400

        pk = kwargs['pk']
        try:
            isinstance(request.session['comment_ids'], list)
        except KeyError:
            self.request.session['comment_ids'] = []
        if pk in self.request.session['comment_ids']:
            data = {'error': _('You have liked that comment before.')}
        else:
            obj.like = F('like') + 1
            obj.save()
            self.request.session['comment_ids'] += [pk]
            data = {'like': self.get_object().like}
            status = 200
        return Response(data, status)


class TagViewSet(mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    # TODO: create actual permissions
    queryset = Tag.objects.select_related('group__owner', 'visitor__visitor')
    serializer_class = serializers.TagSerializer
    pagination_class = None
    permission_classes = [MemberCanServe]


class MemberViewSet(viewsets.ModelViewSet):
    """ Useless currently """
    queryset = Member.objects.select_related('group', 'visitor__visitor')
    serializer_class = serializers.MemberSerializer
    pagination_class = None
    permission_classes = []


class GroupViewSet(OwnerCreateMixin, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrMember]
    # For update use only method patch

    def get_queryset(self):
        """ Pretty complex queryset for retreiving groups """
        visitor = self.request.user
        qs = Group.objects.select_related('owner__visitor').\
            prefetch_related('tag_set', 'member_set__visitor__visitor',
                             'member_set__visitor__vendor__store')
        if self.request.method == 'GET' and not self.kwargs.get('pk', None):
            prefetch = Prefetch('photo_set',
                                queryset=Photo.objects.
                                select_related('original'))

            qs = qs.prefetch_related(prefetch)
            qs = qs.filter(Q(is_private=False) | Q(owner=visitor) |
                           Q(member__visitor=visitor)).distinct()
        else:
            # TODO: optimize for detail view
            qs = qs.prefetch_related('member_set__visitor')
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET' and not self.kwargs.get('pk', None):
            return serializers.GroupListSerializer
        return serializers.GroupDetailSerializer

    def perform_create(self, serializer):
        group = serializer.save()
        members = self.request.data.get('members')
        if members:
            member_batch = (Member(group=group, visitor_id=i) for i in members)
            Member.objects.bulk_create(member_batch)

    @detail_route(methods=['post'])
    def photo_create(self, request, *args, **kwargs):
        """ Handler to save an uploaded photo to the 'group'.
         It is necessary to perform self.get_object to check permission. """

        data = request.data
        data['group'] = self.get_object().id
        data['visitor'] = self.request.user.id

        serializer = serializers.PhotoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)

    @detail_route(methods=['get'])
    def photo_list(self, request, *args, **kwargs):
        """ Photo list for specified group """
        group = self.get_object()
        qs = Photo.p_objects.select_related('visitor__visitor')
        qs = qs.filter(group=group)
        serializer_class = serializers.PhotoListSerializer
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(qs, many=True)
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
            data = {'error': _('{} parameter is required').format(e.message)}
        except Visitor.DoesNotExist:
            data = {'error': _('Matching user does not exists')}
        else:
            member_data = {'visitor': visitor.pk, 'group': pk}
            serializer = serializers.MemberSerializer(data=member_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            status = 201
        return Response(data, status=status)

    @detail_route(methods=['post'])
    def member_vendor_add(self, request, *args, **kwargs):
        """ Add visitor (VENDOR!) to the group by store`s brand name.
         It is necessary to perform self.get_object to check permission.
          Warning: it is not programatically restricted that members of the
          vendor(store) group can instances of the vendor. """
        # TODO: implement restriction.

        pk = self.get_object().id
        status = 400
        try:
            # Argument left with name "username" to be compatible with frontend
            # I do not want to write a completely new frontend for store part.
            username = request.data['username']
            vendor = Vendor.objects.get(store__brand_name=username)
        except KeyError as e:
            data = {'error': _('{} parameter is required').format(e.message)}
        except Vendor.DoesNotExist:
            data = {'error': _('Matching user does not exists')}
        else:
            member_data = {'visitor': vendor.pk, 'group': pk}
            serializer = serializers.MemberSerializer(data=member_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            status = 201
        return Response(data, status=status)

    @detail_route(methods=['post'])
    def member_remove(self, request, *args, **kwargs):
        """ Remove member from group."""
        status = 400
        try:
            member_id = request.data['member']
            member = Member.objects.get(id=member_id, group=self.get_object())
        except KeyError as e:
            data = {'error': _('{} parameter is required').format(e.message)}
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
        data['visitor'] = self.request.user.id

        serializer = serializers.TagSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)

    @list_route(methods=['get'])
    def visitor_list(self, request, *args, **kwargs):
        """ Representation of visitor list. Only visitors """
        status = 400
        try:
            q = request.query_params['q']
            qs = Visitor.objects.filter(~Q(pk=request.user.id),
                                        user__username__startswith=q)[:5]
            serializer = VisitorShortSerializer(qs, many=True)
            data = serializer.data
            status = 200
        except KeyError as e:
            data = {'error': _('{} parameter is required').format(e.message)}
        return Response(data=data, status=status)

    @list_route(methods=['get'])
    def vendor_list(self, request, *args, **kwargs):
        """ Representation of vendor list """
        status = 400
        try:
            q = request.query_params['q']
            qs = Vendor.objects.filter(~Q(pk=request.user.id),
                                       store__brand_name__startswith=q)[:5]

            serializer = VendorStoreSerializer(qs, many=True)
            data = serializer.data
            status = 200
        except KeyError as e:
            data = {'error': _('{} parameter is required').format(e.message)}
        return Response(data=data, status=status)

    @list_route(methods=['get'])
    def my_groups(self, request, *args, **kwargs):

        visitor = self.request.user
        qs = Group.objects.select_related('owner__visitor')
        qs = qs.prefetch_related('tag_set')
        prefetch = Prefetch('photo_set',
                            queryset=Photo.p_objects.select_related('original'))
        qs = qs.prefetch_related(prefetch)
        qs = qs.filter(Q(owner=visitor) | Q(member__visitor=visitor))\
            .distinct()
        serializer_class = self.get_serializer_class()
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def my_groups_short(self, request, *args, **kwargs):
        visitor = self.request.user
        qs = Group.objects.all()
        qs = qs.filter(Q(owner=visitor) | Q(member__visitor=visitor)) \
            .distinct()
        serializer = serializers.GroupShortSerializer(qs, many=True)
        return Response(serializer.data)


class GroupPhotoViewSet(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Photo.objects.select_related('group', 'visitor__visitor')
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
