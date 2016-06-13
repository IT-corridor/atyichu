from __future__ import unicode_literals

from urllib import quote_plus
from django.utils.translation import ugettext as _
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail, mail_admins

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import WeixinSerializer
from .oauth2 import WeixinBackend
from .models import Visitor

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


def index_(request):
    """ Formerly index. Entry point to weixin oauth2 """
    jsapi = JsApi_pub()
    r_url = "http://www.atyichu.com/visitor/openid?url=1"
    redirect_url = '{}://{}{}'.format(request.scheme,
                                      request.get_host(),
                                      reverse('visitor:openid'))
    url = jsapi.createOauthUrlForCode(quote_plus(r_url))
    response = HttpResponseRedirect(url)
    return response


def openid_(request):
    # Get weixin openid then login
    # Else print you are not weixin user
    # This one is working
    # Formerly openid
    url = request.GET.get('url', None)
    redirect = reverse('index')

    if url and url == "2":
        response = HttpResponseRedirect(redirect+'#!/photo/')
    else:
        response = HttpResponseRedirect(redirect+'#!/mirror/')

    if request.user.is_authenticated():
        logout(request)

    code = request.GET.get("code", None)
    if not code:
        return JsonResponse({'error': _('You don`t have weixin code.')})

    jsapi = JsApi_pub()
    jsapi.code = code
    open_id, user_info = jsapi.getOpenid()
    if not open_id:
        return JsonResponse({'error': _('Fail getting openid')})
    try:
        visitor = Visitor.objects.get(weixin=open_id)
    except Visitor.DoesNotExist:
        serializer = WeixinSerializer(data={'weixin': open_id})
        serializer.is_valid(raise_exception=True)
        visitor = serializer.save()
    user = authenticate(weixin=open_id)
    login(request, user)
    # Cookie can set here, delete later
    response.set_cookie('weixin', visitor.weixin, max_age=300)
    return response


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def dummy_api(request):
    return Response(data={'message': 'Hello'}, status=200)


def index(request):
    url = request.GET.get("url")
    weixin_oauth2 = WeixinBackend()
    r_url = "http://www.atyichu.com/visitor/openid?url=1"
    redirect_url = '{}://{}{}'.format(request.scheme,
                                      request.get_host(),
                                      reverse('visitor:openid'))
    redirect_url += '?url={}'.format(url)
    url = weixin_oauth2.get_authorize_uri(r_url)
    mail_admins('From atyichu', 'url is {}'.format(url))
    return HttpResponseRedirect(url)


def openid(request):
    url = request.GET.get("url")

    redirect = reverse('index')

    if url == '2':
        response = HttpResponseRedirect(redirect + '#!/photo/')
    else:
        response = HttpResponseRedirect(redirect + '#!/mirror/')

    if request.user.is_authenticated():
        mail_admins('From atyichu', 'user authenticated')
        return response

    code = request.GET.get("code", None)

    mail_admins('From atyichu', 'code is {}'.format(code))

    if not code:
        return Response({'error': _('You don`t have weixin code.')})

    weixin_oauth = WeixinBackend()
    try:
        mail_admins('From atyichu', 'try to get access_token and openid')
        access_token, openid = weixin_oauth.get_access_token(code)
    except TypeError:
        return Response({'error': _('You got error trying to get openid')})

    user_info = weixin_oauth.get_user_info(access_token, openid)
    mail_admins('From atyichu', user_info)
    try:
        visitor = Visitor.objects.get(weixin=openid)
    except Visitor.DoesNotExist:
        serializer = WeixinSerializer(data={'weixin': openid})
        serializer.is_valid(raise_exception=True)
        visitor = serializer.save()
    user = authenticate(weixin=visitor.weixin)
    login(request, user)
    # Cookie can set here
    response.set_cookie('weixin', visitor.weixin, max_age=300)
    mail_admins('From atyichu', 'Finishing')
    return response
