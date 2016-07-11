from __future__ import unicode_literals

from django.template.defaultfilters import timesince, truncatechars_html
from rest_framework import serializers

from . import models
from visitor.serializers import WeixinSerializer, VisitorShortSerializer
from account.serializers import StoreShortSerializer


class MirrorSerializer(serializers.ModelSerializer):

    is_online = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Mirror
        fields = ('id', 'title', 'latitude', 'longitude', 'is_locked',
                  'is_online', 'last_login')


class CommentSerializer(serializers.ModelSerializer):

    author_data = serializers.SerializerMethodField(read_only=True)

    def get_author_data(self, obj):
        if hasattr(obj.author, 'visitor'):
            serializer = WeixinSerializer(instance=obj.author.visitor,
                                          read_only=True)
            return serializer.data
        elif hasattr(obj.author, 'vendor'):
            serializer = StoreShortSerializer(instance=obj.author.vendor.store,
                                              read_only=True)
            return serializer.data
        else:
            return

    class Meta:
        model = models.Comment


class PhotoSerializer(serializers.ModelSerializer):
    """ A simple photo serializer for creating and editing """
    class Meta:
        model = models.Photo


class PhotoOriginalSerializer(serializers.ModelSerializer):

    descr = serializers.SerializerMethodField(read_only=True)

    def get_descr(self, obj):
        if obj.description:
            return truncatechars_html(obj.description, 150)

    class Meta:
        model = models.Photo
        fields = ('id', 'title', 'photo', 'thumb', 'crop', 'visitor',
                  'description', 'descr')


class PhotoListSerializer(serializers.ModelSerializer):
    """ Works only with PhotoManager or ActivePhotoManager """
    owner = serializers.SerializerMethodField(read_only=True)
    descr = serializers.SerializerMethodField(read_only=True)
    origin = PhotoOriginalSerializer(source='original', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    clone_count = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    def get_descr(self, obj):
        if obj.description:
            return truncatechars_html(obj.description, 150)

    def get_owner(self, obj):
        # TODO: implement for the store (vendor)
        if hasattr(obj.visitor, 'visitor'):
            serializer = VisitorShortSerializer(instance=obj.visitor.visitor,
                                                read_only=True)
            return serializer.data
        elif hasattr(obj.visitor, 'vendor'):
            serializer = StoreShortSerializer(instance=obj.visitor.vendor.store,
                                                read_only=True)
            return serializer.data
        return

    def get_clone_count(self, obj):
        if obj.original_id is not None:
            # Optimize! Really need to optimize.
            return obj.original.clones.count()
        else:
            return obj.clone_count

    class Meta:
        model = models.Photo
        fields = ('id', 'create_date', 'visitor', 'title',
                  'thumb', 'group', 'owner', 'descr', 'creator', 'original',
                  'origin', 'comment_count', 'clone_count', 'like_count',
                  'commodity')


class PhotoDetailSerializer(PhotoListSerializer):
    comments = CommentSerializer(source='comment_set', many=True,
                                 read_only=True)
    owner_thumb = serializers.SerializerMethodField(read_only=True)

    def get_owner_thumb(self, obj):
        if hasattr(obj.visitor, 'visitor'):
            return serializers.ImageField(source='visitor.visitor.thumb',
                                          read_only=True).initial
        elif hasattr(obj.visitor, 'vendor'):
            return serializers.ImageField(source='visitor.vendor.store.thumb',
                                          read_only=True).initial
        return

    class Meta:
        model = models.Photo
        read_only_fields = ('thumb', 'crop', 'cover')


class PhotoCropSerializer(serializers.ModelSerializer):
    """ Works only for GroupListSerializer.
    Needed to get cropped photos from the group."""
    crop = serializers.SerializerMethodField(read_only=True)

    # TODO: optimize code

    def get_crop(self, obj):
        photo = obj
        if photo and photo.original:
            photo = photo.original
        if photo and photo.crop.name:
            request = self.context.get('request', None)
            url = photo.crop.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return

    class Meta:
        model = models.Photo
        fields = ('id', 'crop')

# Group serializers started


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag


class MemberSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='visitor', read_only=True)
    thumb = serializers.SerializerMethodField(read_only=True)

    def get_thumb(self, obj):
        if hasattr(obj.visitor, 'visitor'):
            return serializers.ImageField(source='visitor.visitor.thumb',
                                          read_only=True).initial
        elif hasattr(obj.visitor, 'vendor'):
            return serializers.ImageField(source='visitor.vendor.store.thumb',
                                          read_only=True).initial
        return

    class Meta:
        model = models.Member
        extra_kwargs = {'group': {'write_only': True}}


class GroupSerializer(serializers.ModelSerializer):
    photo_count = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(source='owner', read_only=True)
    thumb = serializers.SerializerMethodField(read_only=True)

    def get_thumb(self, obj):
        photo = obj.photo_set.first()
        if photo and photo.original_id:
            photo = photo.original
        if photo and photo.cover.name:
            request = self.context.get('request', None)
            url = photo.cover.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return

    class Meta:
        model = models.Group


class GroupListSerializer(GroupSerializer):

    overview = serializers.SerializerMethodField(read_only=True)

    def get_overview(self, obj):
        qs = obj.photo_set.all()[1:4]
        serializer = PhotoCropSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = models.Group


class GroupDetailSerializer(GroupSerializer):

    members = MemberSerializer(source='member_set', many=True, read_only=True)
    tags = TagSerializer(source='tag_set', many=True, read_only=True)

    class Meta:
        model = models.Group


class GroupShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Group
        fields = ('id', 'title')
