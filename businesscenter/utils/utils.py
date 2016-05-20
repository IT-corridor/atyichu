from __future__ import unicode_literals

import os
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadPath(object):

    def __init__(self, path, fieldname, suff='', *args):
        self.path = path
        self.suff = suff
        self.fieldname = fieldname
        self.subs = args

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        field = getattr(instance, self.fieldname, None)
        if field:
            filename = '{}-{}.{}'.format(field, self.suff, ext)
        if self.subs:
            subs = tuple(getattr(instance, i).id for i in self.subs)
            sub = '/'.join(str(i) for i in subs)
        else:
            sub = ''
        return os.path.join(self.path, sub, filename)
