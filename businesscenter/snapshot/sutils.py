from __future__ import unicode_literals


import md5
import logging
import datetime


log = logging.getLogger(__name__)


def check_sign(timestamp, checksum):
    key = "sdlfkj9234kjlnzxcv90123098123asldjk"
    sign = md5.new('{}{}'.format(key, timestamp)).hexdigest()
    if checksum != sign:
        log.warn('sign error: client timestamp:{}, '
                 'client sign:{}, server sign:{}')\
            .format(timestamp, checksum, sign)
        return False
    return True
