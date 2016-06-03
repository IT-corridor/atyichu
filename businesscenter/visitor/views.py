from __future__ import unicode_literals

from urllib import quote_plus
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import WeixinSerializer
from .oauth2 import WeixinBackend

from vutils.wzhifuSDK import JsApi_pub


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_view(request):
    # USE openid
    # ALSO with captcha look pretty stupid
    serializer = WeixinSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    visitor = serializer.save()
    user = authenticate(weixin=visitor.weixin)
    user_data = serializer.data
    try:
        login(request, user)
    except Exception as e:
        user_data = {'error': e.message}
    return Response(user_data, status=200)


@api_view(['GET'])
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


def index(request):
    """ Formerly index. Entry point to weixin oauth2 """
    jsapi = JsApi_pub()
    r_url = "http://%s/visitor/openid" % request.get_host()
    redirect_url = '{}://{}{}'.format(request.scheme,
                                      request.get_host(),
                                      reverse('visitor:oauth2'))
    url = jsapi.createOauthUrlForCode(quote_plus(r_url))
    response = HttpResponseRedirect(url)
    return response


def get_oauth2(request):
    # Get weixin openid then login
    # Else print you are not weixin user
    # This one is working
    # Formerly openid
    url = request.get('url', None)
    redirect = reverse('index')

    if url and url == "2":

        response = HttpResponseRedirect(redirect+'#!/photo/')
    else:
        response = HttpResponseRedirect(redirect+'#!/mirror/')

    if request.user.is_authenticated():
        return response

    code = request.GET.get("code", None)
    if not code:
        return Response({'error': _('You don`t have weixin code.')})

    jsapi = JsApi_pub()
    jsapi.code = code
    open_id, user_info = jsapi.getOpenid()
    if not open_id:
        return Response({'error': _('Fail getting openid')})

    serializer = WeixinSerializer(data=open_id)
    serializer.is_valid(raise_exception=True)
    visitor = serializer.save()
    user = authenticate(weixin=open_id)
    login(request, user)
    # Cookie can set here
    response.set_cookie('weixin', visitor.weixin)
    return response


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def dummy_api(request):
    return Response(data={'message': 'Hello'}, status=200)


def index_(request):
    url = request.GET.get("url")
    weixin_oauth2 = WeixinBackend()
    redirect_url = reverse('visitor:oauth2')
    redirect_url += '?url={}'.format(url)
    url = weixin_oauth2.get_authorize_uri(redirect_url)
    return HttpResponseRedirect(url)


def get_oauth2_(request):
    # Get weixin openid then login
    # Else print you are not weixin user
    # This one is working
    # Formerly openid
    url = request.GET.get("url")

    redirect = reverse('snapshot:index')

    if url == '2':
        response = HttpResponseRedirect(redirect + '#!/photos')
    else:
        response = HttpResponseRedirect(reverse(redirect + '#!/mirrors'))

    if request.user.is_authenticated():
        return response

    code = request.GET.get("code", None)
    if not code:
        return Response({'error': _('You don`t have weixin code.')})
    weixin_oauth = WeixinBackend()
    try:
        access_token, openid = weixin_oauth.get_access_token(code)
    except TypeError:
        return Response({'error': _('You got error trying to get openid')})

    user_info = weixin_oauth.get_user_info(access_token, openid)
    serializer = WeixinSerializer(data=openid)
    serializer.is_valid(raise_exception=True)
    visitor = serializer.save()
    user = authenticate(weixin=visitor.weixin)
    login(request, user)
    # Cookie can set here
    response.set_cookie('weixin', visitor.weixin)
    return response