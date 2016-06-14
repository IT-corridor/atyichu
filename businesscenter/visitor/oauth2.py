from __future__ import unicode_literals

import requests
from django.conf import settings
from urllib import urlencode, quote
from urlparse import urljoin


class WeixinBackend(object):

    authorize = {'url': 'https://open.weixin.qq.com/connect/oauth2/authorize',
                 'extra': {'response_type': 'code',
                           'state': 'STATE#wechat_redirect',
                           'scope': 'snsapi_userinfo',
                           }
                 }

    access = {'url': 'https://api.weixin.qq.com/sns/oauth2/access_token',
              'extra': {'grant_type': 'authorization_code'}
              }

    user_url = 'https://api.weixin.qq.com/sns/userinfo'

    appid = settings.WEIXIN_APP_ID
    secret = settings.WEIXIN_SECRET

    def get_authorize_uri(self, redirect_uri):
        params = self.authorize['extra']
        params['redirect_uri'] = redirect_uri
        params['appid'] = self.appid
        return urljoin(self.authorize['url'], '?' + self.format_params(params))

    def get_access_token(self, code):

        params = self.access['extra']
        params['code'] = code
        params['appid'] = self.appid
        params['secret'] = self.secret

        response = requests.get(self.access['url'], params=params)
        data = response.json()
        try:
            access_token = data['access_token']
            openid = data['openid']
        except KeyError:
            return None
        else:
            return access_token, openid

    def get_user_info(self, access_token, openid):
        params = {'access_token': access_token,
                  'openid': openid}

        response = requests.get(self.user_url, params=params)
        data = response.json()
        data['encoding'] = response.encoding
        return data

    def format_params(self, param_map, encode=False):
        li = sorted(param_map)
        buff = [(k, quote(param_map[k]) if encode else param_map[k])
                for k in li]
        return '&'.join('{}={}'.format(k, v) for (k, v) in buff)
