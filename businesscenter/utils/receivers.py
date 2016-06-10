from __future__ import unicode_literals

from .utils import create_thumb, cleanup_files


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
        create_thumb(instance, 'photo', 320)


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
