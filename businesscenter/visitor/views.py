from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import CaptchaSerializer
from vutils.wzhifuSDK import JsApi_pub


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_view(request):
    # USE openid
    # ALSO with captcha look pretty stupid
    serializer = CaptchaSerializer(data=request.data)
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
    """ Formerly index """
    url = request.GET.get("url")
    jsapi = JsApi_pub()
    redirect_url = reverse('visitor:oauth2')
    redirect_url += '?url={}'.format(url)
    url = jsapi.createOauthUrlForCode(redirect_url)
    response = HttpResponseRedirect(url)
    return response


def get_oauth2(request):
    # Get weixin openid then login
    # Else print you are not weixin user
    # This one is working
    # Formerly openid
    url = request.GET.get("url")
    if url == '2':
        response = HttpResponseRedirect(reverse('visitor:dummy'))  # photos
    else:
        response = HttpResponseRedirect(reverse('visitor:dummy')) # mirrors

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

    serializer = CaptchaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    visitor = serializer.save()
    user = authenticate(weixin=visitor.weixin)
    login(request, user)

    return response


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def dummy_api(request):
    data = {'visitor': request.user.visitor}
    return Response(data, status=200)
