from __future__ import unicode_literals

from uuid import uuid4
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Visitor, VisitorExtra
from utils.utils import get_content_file

from django.core.mail import mail_admins


class VisitorExtraSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitorExtra
        exclude = ('visitor',)

    def update(self, instance, validated_data):
        if validated_data.get('expires_in', None):
            validated_data['token_date'] = timezone.now()
        for k, v in validated_data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)

        instance.save()
        return instance


class VisitorSerializer(serializers.ModelSerializer):
    """ Serializer for Weixin user data"""
    avatar_url = serializers.URLField(required=False, write_only=True,
                                      allow_blank=True)
    nickname = serializers.CharField(required=True, write_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        if obj.username:
            return obj.username
        else:
            return obj.user.username

    photo_count = serializers.IntegerField(source='user.photo_set.count',
                                           read_only=True)
    group_count = serializers.IntegerField(source='user.group_set.count',
                                           read_only=True)
    extra = VisitorExtraSerializer(write_only=True, allow_null=True)

    def create(self, validated_data):

        extra = validated_data.pop('extra', None)

        User = get_user_model()
        nickname = smart_unicode(validated_data['nickname'])
        unionid = validated_data['unionid']
        try:
            visitor = Visitor.objects.get(unionid=unionid)
        except Visitor.DoesNotExist:
            # If user with such nickname exists and he has unionid
            if User.objects.filter(username=nickname,
                                   visitor__unionid__isnull=False).exists():
                # generating new username
                username = nickname[0:24] + '_' + uuid4().hex[0:5]
            else:
                username = nickname
            user, created = User.objects.get_or_create(username=username)
            # TODO: handle duplicate names
            if created:
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()

            if hasattr(user, 'visitor'):
                exists = user.visitor.visitorextra_set.\
                    filter(backend=extra['backend']).exists()
                if exists:
                    error = {'detail': _('Such relation already exists.')}
                    raise serializers.ValidationError(error)

                visitor = user.visitor
            else:
                visitor = Visitor.objects.create(user=user, username=nickname,
                                                 unionid=unionid)

        avatar_url = validated_data.pop('avatar_url', None)

        if avatar_url:
            visitor.thumb.delete(True)
            ext, content_file = get_content_file(avatar_url)
            visitor.avatar.save('{}.{}'.format(nickname, ext), content_file)

        if extra:
            VisitorExtra.objects.create(visitor=visitor, **extra)

        return visitor

    def update(self, instance, validated_data):
        # Later make a different view to update profile data
        # Later need to be switched off in the view
        nickname = validated_data.pop('nickname', None)
        if nickname:
            instance.username = nickname

        avatar_url = validated_data.pop('avatar_url', None)
        if avatar_url:
            ext, content_file = get_content_file(avatar_url)
            instance.avatar.save('{}.{}'.format(instance.username,
                                                ext), content_file)
            instance.thumb.delete(True)

        for k, v in validated_data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)

        instance.save()
        return instance

    class Meta:
        model = Visitor
        fields = ('avatar_url', 'nickname', 'thumb', 'username', 'unionid',
                  'avatar', 'group_count', 'photo_count', 'pk', 'extra')
        extra_kwargs = {'thumb': {'read_only': True},
                        'avatar': {'read_only': True},
                        'pk': {'read_only': True},
                        'unionid': {'write_only': True}
                        }


class VisitorShortSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        if obj.username:
            return obj.username
        else:
            return obj.user.username

    class Meta:
        model = Visitor
        fields = ('pk', 'username', 'thumb')
        extra_kwargs = {'pk': {'read_only': True}}
