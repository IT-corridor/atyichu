from __future__ import unicode_literals

from PIL import Image
from django.core.files import File
from io import BytesIO
import imghdr


def create_thumb(sender, **kwargs):
    v = kwargs.get('instance')
    if v.avatar and not v.thumb.name:
        filename = v.avatar.path
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

        name, _ = filename.split('.')
        ext = imghdr.what(filename)
        n_fn = name + '_thumb.' + ext
        img = img.resize((w, h), Image.ANTIALIAS)
        output = BytesIO()
        img.save(output, ext)
        v.thumb.save(n_fn, File(output), save=True)
        output.close()


def cleanup_files(sender, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance = kwargs.get('instance')
    photo = getattr(instance, 'photo', None)
    if photo and hasattr(photo, 'name'):
        photo.delete(save=False)
    thumb = getattr(instance, 'thumb', None)
    if thumb and hasattr(instance, 'thumb'):
        thumb.delete(save=False)
