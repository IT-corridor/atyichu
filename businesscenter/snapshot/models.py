from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from visitor.models import Visitor
from utils.utils import UploadPath
from utils.validators import SizeValidator


class Mirror(models.Model):
    """ OLD Model is sucks. """
    # Formerly known as name
    title = models.CharField(_('Title'), max_length=200, blank=True)
    owner = models.ForeignKey(Visitor, null=True,
                              verbose_name=_('Mirror`s owner'))
    location = models.CharField(_('Location'), max_length=200, blank=True)
    latitude = models.DecimalField(_('Latitude'), max_digits=19,
                                   decimal_places=10, null=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=19,
                                    decimal_places=10, null=True)
    tokens = models.CharField(_('Device tokens'), max_length=200)
    create_date = models.DateTimeField(_('Date created'), auto_now_add=True)
    modify_data = models.DateTimeField(_('Date modified'), auto_now=True)
    lock_date = models.DateTimeField(_('Date locked'), default=timezone.now)
    is_locked = models.BooleanField(_('Locked'), default=True)
    # Formerly online time
    last_login = models.DateTimeField(_('Last login'), default=timezone.now)

    def update_last_login(self):
        # Maybe better to replace the code into manager.
        # Update login, when it is necessary
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def lock(self):
        self.is_locked = True

    class Meta:
        verbose_name = _('Mirror')
        verbose_name_plural = _('Mirrors')
        ordering = ('id', )


class Photo(models.Model):
    path_photo = UploadPath('mirror/photo', 'mirror')
    path_thumb = UploadPath('mirror/photo/thumbs', 'mirror', suff='thumb')
    #user = models.ForeignKey(User, related_name='photo_user')
    mirror = models.ForeignKey(Mirror, verbose_name=_('Mirror'))
    # FOR WHAT IS SESSION??? Looks like it redurant
    session = models.CharField(_('Session id'), max_length=200,
                               unique=True, blank=True)
    title = models.CharField(_('Title'), max_length=200, null=True)
    photo = models.ImageField(_('Photo'), upload_to=path_photo,
                              validators=[SizeValidator(2)])
    thumb = models.ImageField(_('Thumbnail'), upload_to=path_thumb,
                              null=True, blank=True)
    description = models.TextField(_('Description'), null=True,
                                   blank=True, max_length=5000)
    create_date = models.DateTimeField(_('Date created'), auto_now_add=True)
    modify_data = models.DateTimeField(_('Date modified'), auto_now=True)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
        ordering = ('id',)
