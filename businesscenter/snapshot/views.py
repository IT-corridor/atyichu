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
from django.core.urlresolvers import reverse
from django.core.mail import mail_admins
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import Mirror, Photo, Comment
from .serializers import MirrorSerializer, PhotoSerializer, CommentSerializer
from .sutils import check_sign
from utils.permissions import IsVisitor
from vutils.umeng_push import push_unicast
from vutils.wzhifuSDK import JsApi_pub


log = logging.getLogger(__name__)

# API VIEWSETS


class MirrorViewSet(viewsets.GenericViewSet):
    serializer_class = MirrorSerializer
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
        serializer = MirrorSerializer(instance=a_mirrors, many=True)
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
        if mirror.is_available():
            return Response(data={'error': _('Mirror is already locked')},
                            status=400)
        mirror.lock()
        # IT WILL REWRITE OWNER IF DIFFERENT PEOPLE USING MIRROR
        mirror.user = request.user
        mirror.save()
        serializer = MirrorSerializer(mirror)
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
                serializer = MirrorSerializer(mirror)
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


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
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
        # IT IS UGLY!!!
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
        photo = Photo.objects.create(owner=visitor, mirror=mirror)

        log.info('create photo id: {}'.format(photo.id))
        content = {'photo_id': photo.id}
        # SENDING A request to umeng push service,
        # which will push the ANDROID APP.
        send_json, receive_info = push_unicast('571459b267e58e826f000239',
                                               'ydcfc8leufv2efcm4slwmhb2pfffaiop',
                                               mirror.token, json.dumps(content))

        log.info('umeng json: {}, {}'.format(send_json, receive_info))
        return Response(data={'photo_id': photo.id}, status=201)

    def list(self, request, *args, **kwargs):
        """
        get all photo order by time desc
        """
        visitor = request.user.visitor
        photos = Photo.objects.filter(owner=visitor).\
            prefetc_related('comment_set__author')

        serializer = PhotoSerializer(instance=photos, many=True)
        return Response(data=serializer.data)

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
            return Response(data={'error': _})

        # CLEAR THIS
        try:
            photo = Photo.objects.get(id=pid)
        except Photo.DoesNotExist:
            return Response(data={'error': _('Photo does not exist')})

        serializer = PhotoSerializer(instance=photo, data=request.data,
                                     partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_realted('author')
    serializer_class = CommentSerializer
    permission_classes = [IsVisitor]


@api_view(['GET'])
@permission_classes(())
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
