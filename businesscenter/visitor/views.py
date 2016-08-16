from __future__ import unicode_literals

from urllib import quote_plus
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.core.mail import mail_admins
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import VisitorSerializer, VisitorExtraSerializer
from .oauth2 import WeixinBackend, WeixinQRBackend
from .models import Visitor, VisitorExtra
from .permissions import IsVisitorSimple


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_view(request):
    # USE openid
    status = 400
    backend = 'weixin'
    try:
        visitor = Visitor.objects.get(visitorextra__openid=request.data['weixin'],
                                      visitorextra__backend=backend)
        serializer = VisitorSerializer(instance=visitor)
        user_data = serializer.data
        extra = visitor.visitorextra_set.get(backend=backend)
        user = authenticate(weixin=extra.openid)
        login(request, user)
    except KeyError as e:
        user_data = {'weixin': _('Missed param')}
    except Visitor.DoesNotExist:
        user_data = {'weixin': _('User does not exists')}
    except Exception as e:
        user_data = {'error': e.message}
    else:
        status = 200
    return Response(user_data, status=status)


@api_view(['GET'])
@permission_classes((AllowAny,))
def is_authenticated(request):
    if request.user.is_authenticated() \
            and hasattr(request.user, 'visitor'):
        r = True
    else:
        r = False
    return Response({'is_authenticated': r})


@api_view(['GET'])
@permission_classes((AllowAny,))
def logout_view(request):
    logout(request)
    return Response(status=200)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def verify_captcha(request, captcha_key, captcha_value):
    """ PIN VERIFICATION. NO USE FOR NOW """
    # THAT LOGIC LOOKS STUPID. But I leave it for now.
    data = {}
    status = 400
    if not captcha_value:
        data = {'captcha': _('Verification code required')}
    else:
        server_captcha = request.session.get(captcha_key)
        if server_captcha != captcha_value:
            data = {'captcha_error': _('Code is incorrect or has expired')}
        else:
            del request.session[captcha_key]
            status = 200

    return Response(data, status=status)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def dummy_api(request):
    return Response(data={'message': 'Hello'}, status=200)


def index(request):
    """ OAuth2 auhentication with Weixin (Wechat).
        Params:
            qr: if it has some value that can be interpreted like True,
                then we use qr code for authentication.
                Required for the desktop clients.
    """
    url = request.GET.get("qr", "1")
    weixin_oauth2 = WeixinBackend()
    redirect_url = '{}://{}{}'.format(request.scheme,
                                      request.get_host(),
                                      reverse('visitor:openid'))
    redirect_url += '?url={}'.format(url)
    url = weixin_oauth2.get_authorize_uri(redirect_url)
    return HttpResponseRedirect(url)


def openid(request):
    """ OAuth2 handler for weixin """
    redirect = reverse('index')
    qr = request.GET.get("qr", None)

    response = HttpResponseRedirect(redirect + '#!/')

    if request.user.is_authenticated():
        return response

    code = request.GET.get("code", None)

    if not code:
        return JsonResponse({'error': _('You don`t have weixin code.')})

    if qr:
        weixin_oauth = WeixinQRBackend()
        backend = 'weixin_qr'
    else:
        weixin_oauth = WeixinBackend()
        backend = 'weixin'
    try:
        token_data = weixin_oauth.get_access_token(code)
    except TypeError:
        return JsonResponse({'error': _('You got error trying to get openid')})

    user_info = weixin_oauth.get_user_info(token_data['access_token'],
                                           token_data['openid'])
    mail_admins('token_data', str(token_data))
    mail_admins('user_info', str(user_info))
    data = {'avatar_url': user_info.get('headimgurl'),
            'nickname': user_info.get('nickname'),
            'extra': {
                'openid': token_data['openid'],
                'access_token': token_data['access_token'],
                'expires_in': token_data['expires_in'],
                'refresh_token': token_data['refresh_token'],
                'backend': backend,
            }
    }
    try:
        extra = VisitorExtra.objects.get(openid=token_data['openid'],
                                         backend=backend)
        s = VisitorExtraSerializer(instance=extra, data=data['extra'],
                                   partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        visitor = extra.visitor
    except VisitorExtra.DoesNotExist:
        serializer = VisitorSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        visitor = serializer.save()
        extra = None

    if not extra:
        extra = visitor.visitorextra_set.get(backend=backend)
    user = authenticate(weixin=extra.openid, backend=backend)
    login(request, user)
    return response


@api_view(['POST'])
@permission_classes((IsVisitorSimple,))
def update_visitor(request):
    """ Updating user data from weixin """
    # TODO: TEST
    qr = request.data.get('qr', None)
    if qr:
        wx = WeixinQRBackend()
        backend = 'weixin_qr'
    else:
        wx = WeixinBackend()
        backend = 'weixin'
    visitor = request.user.visitor
    extra = VisitorExtra.objects.get(visitor=visitor, backend=backend)
    data = {'access_token': extra.access_token,
            'openid': extra.openid}
    if extra.is_expired():
        data.update(wx.refresh_user_credentials(extra.refresh_token))
        s = VisitorExtraSerializer(instance=extra, data=data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
    user_info = wx.get_user_info(data['access_token'], data['openid'])
    user_data = {
        'avatar_url': user_info.get('headimgurl'),
        'nickname': user_info.get('nickname'),
    }
    serializer = VisitorSerializer(instance=visitor,
                                   data=user_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)


@api_view(['GET'])
@permission_classes((IsVisitorSimple,))
def get_me(request):
    """ Provides personal user data, username and thumb """
    visitor = request.user.visitor
    serializer = VisitorSerializer(instance=visitor)
    return Response(data=serializer.data)


def test_auth(request):
    host = request.get_host()
    if host == '127.0.0.1:8000':
        extra = VisitorExtra.objects.get(backend='weixin', openid='weixin')
        user = authenticate(weixin=extra.openid)
        login(request, user)
        response = HttpResponseRedirect('/#!/')
        return response
    raise PermissionDenied
