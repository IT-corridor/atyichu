from __future__ import unicode_literals


def cleanup_files(sender, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance = kwargs.get('instance')
    pic = getattr(instance, 'avatar', None)

    if pic is None:
        pic = getattr(instance, 'logo', None)

    if pic and hasattr(pic, 'name'):
        pic.delete(save=False)
