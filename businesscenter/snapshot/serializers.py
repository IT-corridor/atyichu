from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class MirrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Mirror
        fields = ('id', 'name', 'latitude', 'longitude', 'is_locked')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Photo
