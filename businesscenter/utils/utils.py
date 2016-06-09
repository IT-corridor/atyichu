from __future__ import unicode_literals, division

import os
import imghdr
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.utils.deconstruct import deconstructible



@deconstructible
class UploadPath(object):

    def __init__(self, path, fieldname=None, suff='', *args):
        self.path = path
        self.suff = suff
        self.fieldname = fieldname
        self.subs = args

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if self.fieldname:
            field = getattr(instance, self.fieldname, None)
            if field:
                filename = '{}-{}.{}'.format(field, self.suff, ext)
        if self.subs:
            subs = tuple(getattr(instance, i).pk for i in self.subs)
            sub = '/'.join(str(i) for i in subs)
        else:
            sub = ''
        return os.path.join(self.path, sub, filename)


def cleanup_files(instance, fieldname):
    # Pass false so FileField doesn't save the model.
    field = getattr(instance, fieldname)

    if field and hasattr(field, 'name'):
        field.delete(save=False)
    thumb = getattr(instance, 'thumb', None)
    if thumb and hasattr(instance, 'thumb'):
        thumb.delete(save=False)


def create_thumb(instance, fieldname):
    field = getattr(instance, fieldname)
    if field and not instance.thumb.name:
        filename = field.path
        img = Image.open(filename)
        w, h = img.size
        m = 100
        if w > m:
            ratio = m / w
            w = m
            h = int(h * ratio)

        if h > m:
            ratio = m / h
            h = m
            w = int(w * ratio)

        name, _ = field.name.split('.')
        ext = imghdr.what(filename)
        n_fn = name + '_thumb.' + ext
        img = img.resize((w, h), Image.ANTIALIAS)
        output = BytesIO()
        img.save(output, ext)
        instance.thumb.save(n_fn, File(output), save=True)
        output.close()
