from __future__ import unicode_literals, division

import os
import imghdr
import requests
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files import File
from django.utils.deconstruct import deconstructible
from django.core.files.base import ContentFile



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
    if thumb and hasattr(thumb, 'name'):
        thumb.delete(save=False)

    crop = getattr(instance, 'crop', None)
    if crop and hasattr(crop, 'name'):
        crop.delete(save=False)


def cleanup_if_none(instance, fieldname):
    """If main picture is None, remove others (crop, and thumb)"""
    field = getattr(instance, fieldname)

    if not field.name:
        thumb = getattr(instance, 'thumb', None)
        if thumb:
            thumb.delete()

        crop = getattr(instance, 'crop', None)
        if crop:
            crop.delete()


def create_thumb(instance, fieldname, m=100):
    field = getattr(instance, fieldname)
    if field and not instance.thumb.name:
        filename = field.path
        img = Image.open(filename)
        w, h = img.size
        if w > m:
            ratio = m / w
            w = m
            h = int(h * ratio)

        if h > m:
            ratio = m / h
            h = m
            w = int(w * ratio)

        filepath, _ = field.name.split('.')
        name = filepath.split('/')[-1]
        ext = imghdr.what(filename)
        n_fn = name + '_thumb.' + ext
        img = img.resize((w, h), Image.ANTIALIAS)
        output = BytesIO()
        img.save(output, ext)
        instance.thumb.save(n_fn, File(output), save=True)
        output.close()


def create_crop(instance, fieldname, m=100):
    field = getattr(instance, fieldname)
    if field and not instance.crop.name:
        filename = field.path
        img = Image.open(filename)
        w, h = img.size
        ratio_w = m / w
        ratio_h = m / h
        if ratio_w < ratio_h:
            cropped = ImageOps.fit(img, (m, m), Image.ANTIALIAS,
                                   centering=(0.0, ratio_h))
        else:
            cropped = ImageOps.fit(img, (m, m), Image.ANTIALIAS,
                                   centering=(ratio_w, 0.0))
        filepath, _ = field.name.split('.')
        name = filepath.split('/')[-1]
        ext = imghdr.what(filename)
        n_fn = name + '_crop.' + ext

        output = BytesIO()
        cropped.save(output, ext)
        instance.crop.save(n_fn, File(output), save=True)
        output.close()


def get_content_file(url):
    r = requests.get(url)
    ext = r.headers['Content-Type'].split('/')[-1]
    return ext, ContentFile(r.content)
