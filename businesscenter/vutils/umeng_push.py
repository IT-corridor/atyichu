# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import time

import hashlib
import requests
import json
import urllib2
import datetime
import pusher
import os
import cgi

from django.conf import settings


# {"appkey": "56f3b94267e58e49270019e7", "production_mode": "false",
# "description": "testaaa", "type": "unicast",
# "payload": {"display_type": "message", "body": {"custom": "aaabbb"}},
# "policy": {"expire_time": "2016-04-12 17:07:55"},
# "device_tokens": "AjzbcO4OoVNsKfYPdSoilaohG3pjlfPCBdhpXGaBiGMs"}


def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()


def push_unicast(device_token, text):
    timestamp = int(time.time() * 1000)
    method = 'POST'
    url = 'http://msg.umeng.com/api/send'

    params = {
        'appkey': settings.UMENG_APP_KEY,
        'timestamp': timestamp,
        'device_tokens': device_token,
        # "production_mode":"false",
        'type': 'unicast',
        "payload": {
            "display_type": "message",
            "body": {
                "custom": text
            }
        },
        # "policy":
        # {
        #    "expire_time":"%s"%(datetime.datetime.now())
        # },
        "description": "жµ‹иЇ•еЌ•ж’­ж¶€жЃЇ-Android"
    }

    post_body = json.dumps(params)
    sign = md5('%s%s%s%s' % (
    method, url, post_body, settings.UMENG_APP_MASTER_SECRET))
    success_info = ""

    try:
        r = urllib2.urlopen(url + '?sign=' + sign, data=post_body)
        success_info = r.read()
        print success_info
    except urllib2.HTTPError, e:
        print e.reason, e.read()
    except urllib2.URLError, e:
        print e.reason
    return post_body, success_info

def trigger_notification():
    app_id = '236840'#os.environ.get('PUSHER_APP_ID')
    key = "4c8e6d909a1f7ccc44ed"#os.environ.get('PUSHER_APP_KEY')
    secret = "119328e419074c206e29"#os.environ.get('PUSHER_APP_SECRET')

    p = pusher.Pusher(app_id=app_id, key=key, secret=secret)

    message =  cgi.escape(request.form['message'])
    p.trigger('notifications', 'new_notification', {'message': message})
    return "Notification triggered!"
