from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Visitor
from utils.utils import get_content_file


# PART 1 FEATURES #
class WeixinSerializer(serializers.ModelSerializer):
    avatar_url = serializers.URLField(required=False, write_only=True)
    nickname = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    # Added 23.06.2013
    photo_count = serializers.IntegerField(source='photo_set.count',
                                           read_only=True)
    group_count = serializers.IntegerField(source='group_set.count',
                                           read_only=True)

    # EXTEND LATER
    # We assume that we get a validated data from weixin open id
    def create(self, validated_data):

        user_model = get_user_model()
        nickname = smart_unicode(validated_data['nickname'])
        # In this case we assume that one user can have only one weixin account
        user = user_model(username=nickname)
        password = user_model.objects.make_random_password()
        user.set_password(password)
        user.save()
        visitor = Visitor.objects.create(weixin=validated_data['weixin'],
                                         user=user,
                                         access_token=validated_data['access_token'],
                                         expires_in=validated_data['expires_in'])
        avatar_url = validated_data.pop('avatar_url', None)
        if avatar_url:
            ext, content_file = get_content_file(avatar_url)
            visitor.avatar.save('{}.{}'.format(nickname, ext), content_file)
        return visitor

    def update(self, instance, validated_data):
        # Later make a different view to update profile data
        # Later need to be switched off in the view
        nickname = validated_data.pop('nickname', None)
        user = self.instance.user
        if nickname:
            user.username = nickname
            user.save()
        if not instance.avatar.name:
            avatar_url = validated_data.pop('avatar_url', None)
            if avatar_url:
                ext, content_file = get_content_file(avatar_url)
                instance.avatar.save('{}.{}'.format(user.username,
                                                    ext), content_file)

        if validated_data.get('expires_in', None):
            instance.token_date = timezone.now()

        for k, v in validated_data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)

        instance.save()
        return instance

    class Meta:
        model = Visitor
        fields = ('weixin', 'avatar_url', 'nickname', 'thumb', 'username',
                  'access_token', 'expires_in', 'refresh_token', 'avatar',
                  'group_count', 'photo_count', 'pk')
        extra_kwargs = {'thumb': {'read_only': True},
                        'weixin': {'write_only': True},
                        'access_token': {'write_only': True},
                        'expires_in': {'write_only': True},
                        'refresh_token': {'write_only': True},
                        'avatar': {'read_only': True},
                        'pk': {'read_only': True}
                        }


class VisitorShortSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Visitor
        fields = ('pk', 'username')
        extra_kwargs = {'pk': {'read_only': True}}
