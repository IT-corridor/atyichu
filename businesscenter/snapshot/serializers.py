from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class MirrorSerializer(serializers.ModelSerializer):

    is_online = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Mirror
        fields = ('id', 'title', 'latitude', 'longitude', 'is_locked',
                  'is_online')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Photo
