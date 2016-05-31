from django.contrib.auth.models import User
from .models import Visitor
from .serializers import WeixinSerializer


class WeixinBackend(object):
    """
    Authenticate with weixin id. Base is "auth.User" model. It is strict.
    """

    def authenticate(self, weixin=None):
        try:
            visitor = Visitor.objects.get(weixin=weixin)
            user = visitor.user
        except Visitor.DoesNotExist:
            user = None
        return user

    def get_user(self, pk):
        try:
            return Visitor.objects.get(pk=pk).user
        except User.DoesNotExist:
            return None