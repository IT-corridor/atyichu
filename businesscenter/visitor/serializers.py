from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Visitor


# PART 1 FEATURES #

class WeixinSerializer(serializers.ModelSerializer):
    # EXTEND LATER
    # We assume that we get a validated data from weixin open id
    def create(self, validated_data):
        try:
            visitor = Visitor.objects.get(weixin=validated_data['weixin'])
        except Visitor.DoesNotExist:
            user_model = get_user_model()
            user = user_model(username=validated_data['weixin'])
            password = user_model.objects.make_random_password()
            user.set_password(password)
            user.save()
            visitor = Visitor.objects.create(weixin=validated_data['weixin'],
                                             user=user)
        return visitor

    class Meta:
        model = Visitor
        fields = ('weixin',)
