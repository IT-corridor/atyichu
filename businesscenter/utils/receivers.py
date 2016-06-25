from __future__ import unicode_literals

from .utils import create_thumb, create_crop, cleanup_files, cleanup_if_none


def create_thumb_avatar(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if instance:
        create_thumb(instance, 'avatar')


def create_thumb_photo(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if instance:
        create_thumb(instance, 'photo')


def create_thumb_photo_320(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if instance:
        create_crop(instance, 'photo', 320, 'thumb')


def create_thumb_avatar_320(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if instance:
        create_thumb(instance, 'avatar', 320)


def create_crop_photo_100(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if instance:
        create_crop(instance, 'photo', 100)


def cleanup_files_avatar(sender, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance = kwargs.get('instance', None)
    if instance:
        cleanup_files(instance, 'avatar')


def cleanup_files_photo(sender, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance = kwargs.get('instance', None)
    if instance:
        cleanup_files(instance, 'photo')


def cleanup_if_avatar_is_none(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if instance:
        cleanup_if_none(instance, 'avatar')