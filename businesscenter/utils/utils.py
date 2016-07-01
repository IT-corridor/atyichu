from __future__ import unicode_literals, division

import os
import imghdr
import requests
from io import BytesIO
from PIL import Image, ImageOps, ExifTags
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
        img = rotate_image(img)
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


def create_crop(instance, input_field, m=100, output_field='crop'):
    crop_field = getattr(instance, output_field)
    field = getattr(instance, input_field)
    if field and not crop_field.name:
        filename = field.path
        img = Image.open(filename)
        img = rotate_image(img)
        w, h = img.size
        if w > h:
            # Ratio does not really matter because it pretty small
            # Crop width
            # Also it can be used ratio_w instead 0.5
            centering = (0.0, 0.5)
        else:
            # Crop height
            centering = (0.5, 0.5)
        cropped = ImageOps.fit(img, (m, m), Image.ANTIALIAS,
                               centering=centering)
        filepath, _ = field.name.split('.')
        name = filepath.split('/')[-1]
        ext = imghdr.what(filename)
        n_fn = name + '_' + output_field + '.' + ext

        output = BytesIO()
        cropped.save(output, ext)
        crop_field.save(n_fn, File(output), save=True)
        output.close()


def get_content_file(url):
    r = requests.get(url)
    ext = r.headers['Content-Type'].split('/')[-1]
    return ext, ContentFile(r.content)


def rotate_image(image):
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if exif is not None:
            # PYTHON 2!
            # tag = filter(lambda x: x[1] == 'Orientation', ExifTags.TAGS.items())[0]
            # key, value = tag
            # Exif orientation tag
            key = 0x0112
            exif_data = dict(image._getexif().items())
            orientation_tag = exif_data.get(key)
            if orientation_tag:
                if orientation_tag == 3:
                    image = image.rotate(180, expand=True)
                elif orientation_tag == 6:
                    image = image.rotate(270, expand=True)
                elif orientation_tag == 8:
                    image = image.rotate(90, expand=True)
    return image