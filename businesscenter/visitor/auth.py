from django.contrib.auth.models import User
from .models import Visitor, VisitorExtra
from .serializers import WeixinSerializer


class WeixinBackend(object):
    """
    Authenticate with weixin id. Base is "auth.User" model. It is strict.
    """

    def authenticate(self, weixin=None, backend='weixin'):
        try:
            extra = VisitorExtra.objects.select_related('visitor__user')\
                .get(openid=weixin, backend=backend)
            user = extra.visitor.user
        except VisitorExtra.DoesNotExist:
            user = None
        return user

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
