from __future__ import unicode_literals

from datetime import timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from visitor.models import Visitor
from utils.utils import UploadPath
from utils.validators import SizeValidator


class MirrorQuerySet(models.query.QuerySet):

    def lock(self):
        return self.update(is_locked=True, lock_date=timezone.now(),
                           last_login=timezone.now())

    def unlock(self):
        return self.update(is_locked=False, last_login=timezone.now())


class MirrorManager(models.Manager):

    def get_queryset(self):
        return MirrorQuerySet(self.model, using=self._db)

    def lock(self):
        return self.get_queryset().lock()

    def unlock(self):
        return self.get_queryset().unlock()

    def get_by_distance(self, lat, lon):
        # IT IS NOT MY QUERY
        sql = "SELECT * FROM (SELECT id,longitude,latitude, is_locked, owner_id, " \
               "ROUND(6378.138*2*ASIN(SQRT(POW(SIN((%s*PI()/" \
              "180-latitude*PI()/180)/2),2)+COS(%s*PI()/180)*COS(latitude*PI()/180)" \
               "*POW(SIN((%s*PI()/180-longitude*PI()/180)/2),2)))*1000) " \
              "AS distance FROM snapshot_mirror ORDER BY distance LIMIT 10) s " \
              "WHERE  distance < 500"
        return self.raw(sql, [lat, lat, lon])


class Mirror(models.Model):
    """ OLD Model is sucks. """
    #TODO: One mirror can refer many users, so owner field maybe redundant here
    # Formerly known as name
    title = models.CharField(_('Title'), max_length=200, blank=True)
    owner = models.ForeignKey(Visitor, null=True,
                              verbose_name=_('Mirror`s owner'))
    location = models.CharField(_('Location'), max_length=200, blank=True)
    latitude = models.DecimalField(_('Latitude'), max_digits=19,
                                   decimal_places=10, null=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=19,
                                    decimal_places=10, null=True)
    # Formerly known as device_tokens
    token = models.CharField(_('Device tokens'), max_length=200)
    create_date = models.DateTimeField(_('Date created'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date modified'), auto_now=True)
    lock_date = models.DateTimeField(_('Date locked'), default=timezone.now)
    is_locked = models.BooleanField(_('Locked'), default=True)
    # Formerly online time
    last_login = models.DateTimeField(_('Last login'), default=timezone.now)

    objects = MirrorManager()

    def update_last_login(self):
        # Maybe better to replace the code into manager.
        # Update login, when it is necessary
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def lock(self):
        self.is_locked = True
        self.lock_date = timezone.now()
        self.save(update_fields=['is_locked', 'is_locked'])

    def is_available(self):
        return self.is_locked and \
               timezone.now() < (self.modify_date + timedelta(minutes=1))

    def is_online(self):
        return timezone.now() < (self.last_login + timedelta(seconds=66))

    def is_overtime(self):
        # Looks like something stupid
        # It checks only locked mirrors, so maybe in this
        # condition you have to remove "mirror.is_locked"
        if self.is_locked and \
                timezone.now() < (self.modify_date + timedelta(minutes=1)):
            return True
        return False

    def __unicode__(self):
        return self.token

    class Meta:
        verbose_name = _('Mirror')
        verbose_name_plural = _('Mirrors')
        ordering = ('-modify_date', )


class Photo(models.Model):
    path_photo = UploadPath('mirror/photo', 'mirror')
    path_thumb = UploadPath('mirror/photo/thumbs', 'mirror', suff='thumb')
    owner = models.ForeignKey(Visitor, null=True,
                              verbose_name=_('Mirror`s owner'))
    mirror = models.ForeignKey(Mirror, verbose_name=_('Mirror'))
    # FOR WHAT IS SESSION??? Looks like it redurant
    session = models.CharField(_('Session id'), max_length=200,
                               unique=True, blank=True)
    title = models.CharField(_('Title'), max_length=200, null=True)
    photo = models.ImageField(_('Photo'), upload_to=path_photo,
                              null=True, blank=True,
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
        ordering = ('create_date', 'id')
