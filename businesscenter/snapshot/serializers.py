from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class MirrorSerializer(serializers.ModelSerializer):

    is_online = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Mirror
        fields = ('id', 'title', 'latitude', 'longitude', 'is_locked',
                  'is_online')


class CommentSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='author__weixin', read_only=True)

    class Meta:
        model = models.Comment


class PhotoSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Photo
