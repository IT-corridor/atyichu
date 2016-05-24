from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from rest_framework import serializers
from . import models
from django.contrib.auth.password_validation import validate_password as vp
from django.db import transaction


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

    url = serializers.HyperlinkedIdentityField(view_name='account:store-detail')
    district = DistrictSerializer()
    location = serializers.CharField(source='get_location', read_only=True)

    def create(self, validated_data):
        with transaction.atomic():
            district_args = validated_data.pop('district')
            city_args = district_args.pop('city')
            state_args = city_args.pop('state')

            state, _ = models.State.objects.get_or_create(**state_args)

            city_args['state'] = state

            city, c = models.City.objects.get_or_create(**city_args)

            district_args['city'] = city

            district, c = models.District.objects.get_or_create(
                **district_args)

            validated_data['district'] = district
            store = self.Meta.model.objects.create(**validated_data)
            return store

    def update(self, instance, validated_data):
        with transaction.atomic():
            district_args = validated_data.pop('district', None)

            for k, v in validated_data.items():
                setattr(instance, k, v)

            if district_args:
                self.check_key_title('district', **district_args)
                try:
                    city_args = district_args.pop('city')
                    self.check_key_title('city', **city_args)

                    state_args = city_args.pop('state')

                    state, c = models.State.objects.get_or_create(**state_args)
                    self.check_key_title('state', **state_args)

                    city_args['state'] = state

                    city, c = models.City.objects.get_or_create(**city_args)

                    district_args['city'] = city
                except KeyError as e:
                    raise serializers.ValidationError(
                        {e.message: _('This field is required.')})
                district, c = models.District.objects.get_or_create(**district_args)

                instance.district = district

        instance.save()
        return instance

    def check_key_title(self, key, **kwargs):
        if 'title' not in kwargs:
            raise serializers.ValidationError(
                {key: _('This field is required.')})

    class Meta:
        model = models.Store


class UserCreateSerializer(serializers.ModelSerializer):
    """ Serializer for creating new profile """

    url = serializers.HyperlinkedIdentityField(view_name='account:profile-detail')
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)
    store = StoreSerializer(read_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password':
                                                   _('Passwords do not match')})
        return attrs

    def validate_password(self, value):
        """ Validate password with django password validation """
        vp(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = models.Vendor
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   'user_permissions', )
        write_only_fields = ('password',)
        read_only_fields = ('date_joined', 'last_login')


class UserUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for update account """
    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

    class Meta:
        model = models.Vendor
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   'user_permissions', 'password',)
        read_only_fields = ('date_joined', 'last_login')


class UserPasswordSerializer(serializers.ModelSerializer):
    """ Serializer for resetting user`s password """
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)
    new_password = serializers.CharField(allow_blank=False, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password':
                                                   _('Passwords do not match')})
        return attrs

    def validate_password(self, value):
        vp(value)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    class Meta:
        model = models.Vendor
        fields = ('password', 'confirm_password', 'new_password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('username',)

