from __future__ import unicode_literals

from rest_framework import serializers

from . import models
from visitor.serializers import WeixinSerializer


class MirrorSerializer(serializers.ModelSerializer):

    is_online = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Mirror
        fields = ('id', 'title', 'latitude', 'longitude', 'is_locked',
                  'is_online', 'last_login')


class CommentSerializer(serializers.ModelSerializer):

    author_data = WeixinSerializer(source='author', read_only=True)

    class Meta:
        model = models.Comment


class PhotoListSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(source='comment_set.count',
                                             read_only=True)

    class Meta:
        model = models.Photo
        fields = ('id', 'create_date', 'comment_count',
                  'visitor', 'title', 'thumb',
                  )


class PhotoDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(source='comment_set', many=True,
                                 read_only=True)

    class Meta:
        model = models.Photo


# Group serializers started

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Member


class GroupDetailSerializer(serializers.ModelSerializer):

    members = MemberSerializer(many=True, read_only=True)
    tags = TagSerializer(source='tag_set', many=True, read_only=True)

    class Meta:
        model = models.Group


class GroupListSerializer(GroupDetailSerializer):

    members = MemberSerializer(many=True, read_only=True)
    tags = TagSerializer(source='tag_set', many=True, read_only=True)
    photo_set = PhotoListSerializer(many=True, read_only=True)

    class Meta:
        model = models.Group
