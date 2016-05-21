from __future__ import unicode_literals

from django.contrib.auth.models import Group


def cleanup_files(sender, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance = kwargs.get('instance')
    pic = getattr(instance, 'avatar', None)

    if pic is None:
        pic = getattr(instance, 'logo', None)

    if pic and hasattr(pic, 'name'):
        pic.delete(save=False)


def add_to_vendor_group(sender, instance=None, created=False, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='vendors'))
