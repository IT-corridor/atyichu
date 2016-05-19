from django.utils.translation import ugettext as _
from rest_framework import serializers
from . import models
from django.contrib.auth.password_validation import validate_password as vp


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.State


class CitySerializer(serializers.ModelSerializer):

    state = StateSerializer()

    class Meta:
        model = models.City


class DistrictSerializer(serializers.ModelSerializer):

    city = CitySerializer()

    class Meta:
        model = models.District


class StoreSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()
    location = serializers.CharField(source='get_location', read_only=True)

    class Meta:
        model = models.Store


class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='account:profile-detail')
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)
    store = StoreSerializer(read_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password':
                                                   _('Passwords do not match')})
        return attrs

    def validate_password(self, value):
        vp(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = models.Profile
        fields = ('url', 'password', 'confirm_password', 'store',
                  'username')
        write_only_fields = ('password',)
