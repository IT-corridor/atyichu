# -*- coding: utf-8 -*-

import requests
import datetime
import pytz
import hashlib
import operator
from django.conf import settings


class TaoSMSAPI(object):

    def __init__(self, app_key=None, app_secret=None):
        self.url = 'http://gw.api.taobao.com/router/rest'
        self.app_key = settings.TAO_SMS_KEY if not app_key else app_key
        self.secret = settings.TAO_SMS_SECRET if not app_secret else app_secret

    def get_payload(self, **kwargs):
        """ Do not forget sms_param"""
        china = pytz.timezone('Asia/Shanghai')
        timestamp = datetime.datetime.now(tz=china)\
            .strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'app_key': self.app_key,
            'format': 'json',
            'method': 'alibaba.aliqin.fc.sms.num.send',
            'sign_method': 'md5',
            'timestamp': timestamp,
            'v': '2.0',
            'sms_type': 'normal'
        }
        data.update(kwargs)
        sign = self.get_sign(data)
        data['sign'] = sign
        return data

    def get_sign(self, data):
        """ Write a comment """
        s = ''.join(k + v for k, v in sorted(data.items(),
                                             key=operator.itemgetter(0)))
        s = '{}{}{}'.format(self.secret, s, self.secret)
        sign = hashlib.md5(s).hexdigest().upper()
        return sign

    def send(self, phone_number, sms_param):
        """ Send sms"""
        extra = {
            'sms_param': sms_param,
            'sms_template_code': 'SMS_13500018',
            'partner_id': 'apidoc',
            'extend': '123456',
            'rec_num': phone_number,
            'sms_free_sign_name': '阿里大于',
        }
        payload = self.get_payload(**extra)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        }

        r = requests.post(self.url, data=payload, headers=headers)

        # assert r.status_code == 200

        return r.json()

if __name__ == '__main__':
    # TODO: remove before push

    app_key = '23438643'
    app_secret = '785f1713c9472a73596336a9f5e3eeeb'

    sms_api = TaoSMSAPI(app_key, app_secret)
    result = sms_api.send('13521405982',
                          '{\"code\":\"1234\",\"product\":\"ATYICHU\"}')

    print (result)