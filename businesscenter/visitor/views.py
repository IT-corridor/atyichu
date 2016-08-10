from __future__ import unicode_literals

from urllib import quote_plus
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, mail_admins
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import WeixinSerializer
from .oauth2 import WeixinBackend, WeixinQRBackend
from .models import Visitor
from .permissions import IsVisitorSimple


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_view(request):
    # USE openid
    status = 400
    try:
        visitor = Visitor.objects.get(weixin=request.data['weixin'])
        serializer = WeixinSerializer(instance=visitor)
        user_data = serializer.data
        user = authenticate(weixin=visitor.weixin)
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
    url = request.GET.get("url", "1")
    weixin_oauth2 = WeixinBackend()
    redirect_url = '{}://{}{}'.format(request.scheme,
                                      request.get_host(),
                                      reverse('visitor:openid'))
    redirect_url += '?url={}'.format(url)
    url = weixin_oauth2.get_authorize_uri(redirect_url)
    return HttpResponseRedirect(url)


def openid(request):
    redirect = reverse('index')

    response = HttpResponseRedirect(redirect + '#!/')

    if request.user.is_authenticated():
        return response

    code = request.GET.get("code", None)

    if not code:
        return JsonResponse({'error': _('You don`t have weixin code.')})

    weixin_oauth = WeixinBackend()
    try:
        token_data = weixin_oauth.get_access_token(code)
    except TypeError:
        return JsonResponse({'error': _('You got error trying to get openid')})

    user_info = weixin_oauth.get_user_info(token_data['access_token'],
                                           token_data['openid'])
    data = {'avatar_url': user_info.get('headimgurl'),
            'nickname': user_info.get('nickname'),
            'weixin': token_data['openid'],
            'access_token': token_data['access_token'],
            'expires_in': token_data['expires_in'],
            'refresh_token': token_data['refresh_token']}
    try:
        visitor = Visitor.objects.get(weixin=token_data['openid'])
    except Visitor.DoesNotExist:
        serializer = WeixinSerializer(data=data)
    else:
        serializer = WeixinSerializer(instance=visitor, data=data)

    serializer.is_valid(raise_exception=True)
    visitor = serializer.save()
    user = authenticate(weixin=visitor.weixin)
    login(request, user)
    # Cookie will be set on the front-end side
    #response.set_cookie('weixin', visitor, max_age=7200)
    return response


@api_view(['GET', 'POST'])
def openid_qr(request):
    mail_admins('test qr', 'open the qr handler')

    if request.user.is_authenticated():
        return Response(status=400)

    code = request.GET.get("code", None)

    if not code:
        return JsonResponse({'error': _('You don`t have weixin code.')})

    weixin_oauth = WeixinQRBackend()
    try:
        token_data = weixin_oauth.get_access_token(code)
    except TypeError:
        return JsonResponse({'error': _('You got error trying to get openid')})

    user_info = weixin_oauth.get_user_info(token_data['access_token'],
                                           token_data['openid'])
    mail_admins('info data', str(user_info))
    data = {'avatar_url': user_info.get('headimgurl'),
            'nickname': user_info.get('nickname'),
            'weixin': token_data['openid'],
            'access_token': token_data['access_token'],
            'expires_in': token_data['expires_in'],
            'refresh_token': token_data['refresh_token'],
            'backend': 'weixin_qr'}
    try:
        visitor = Visitor.objects.get(weixin=token_data['openid'])
    except Visitor.DoesNotExist:
        serializer = WeixinSerializer(data=data)
    else:
        serializer = WeixinSerializer(instance=visitor, data=data)

    serializer.is_valid(raise_exception=True)
    visitor = serializer.save()
    user = authenticate(weixin=visitor.weixin)
    login(request, user)
    # Cookie will be set on the front-end side
    #response.set_cookie('weixin', visitor, max_age=7200)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsVisitorSimple,))
def update_visitor(request):
    """ Updating user data from weixin """
    wx = WeixinBackend()
    visitor = request.user.visitor
    data = {'access_token': visitor.access_token,
            'weixin': visitor.weixin}
    if visitor.is_expired():
        data.update(wx.refresh_user_credentials(visitor.refresh_token))
    user_info = wx.get_user_info(data['access_token'], data['weixin'])
    data.update(user_info)
    serializer = WeixinSerializer(instance=visitor, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)


@api_view(['GET'])
@permission_classes((IsVisitorSimple,))
def get_me(request):
    """ Provides personal user data, username and thumb """
    visitor = request.user.visitor
    serializer = WeixinSerializer(instance=visitor)
    return Response(data=serializer.data)


def test_auth(request):
    host = request.get_host()
    if host == '127.0.0.1:8000':
        visitor = Visitor.objects.get(weixin='weixin2')
        user = authenticate(weixin=visitor.weixin)
        login(request, user)
        response = HttpResponseRedirect('/#!/')
        response.set_cookie('weixin', visitor.weixin, max_age=7200)
        return response
    raise PermissionDenied
