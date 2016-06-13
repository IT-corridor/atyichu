from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Visitor
from utils.utils import get_content_file

# PART 1 FEATURES #
class WeixinSerializer(serializers.ModelSerializer):
    avatar_url = serializers.URLField(required=False)
    nickname = serializers.CharField()

    # EXTEND LATER
    # We assume that we get a validated data from weixin open id
    def create(self, validated_data):

        user_model = get_user_model()
        user = user_model(username=validated_data['nickname'])
        password = user_model.objects.make_random_password()
        user.set_password(password)
        user.save()
        visitor = Visitor.objects.create(weixin=validated_data['weixin'],
                                         user=user)
        filename = validated_data['nickname']
        avatar_url = validated_data.pop('avatar_url', None)
        if avatar_url:
            ext, content_file = get_content_file(avatar_url)
            visitor.avatar.save('{}.{}'.format(filename, ext), content_file)
        return visitor

    def update(self, instance, validated_data):
        # Later make a different view to update profile data
        # Later need to be switched off in the view
        user = self.instance.user
        if user.username == self.instance.weixin:
            user.username = validated_data['nickname']
            user.save()
        if not instance.avatar.name:
            avatar_url = validated_data.pop('avatar_url', None)
            if avatar_url:
                ext, content_file = get_content_file(avatar_url)
                instance.avatar.save('{}.{}'.format(validated_data['nickname'],
                                                    ext), content_file)
        instance.save()
        return instance



    class Meta:
        model = Visitor
        fields = ('weixin', 'avatar_url', 'nickname')
