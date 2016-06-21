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
        sql = "SELECT * FROM (SELECT id,longitude,latitude, " \
              "is_locked, owner_id, " \
               "ROUND(6378.138*2*ASIN(SQRT(POW(SIN((%s*PI()/" \
              "180-latitude*PI()/180)/2),2)+COS(%s*PI()/180)" \
              "*COS(latitude*PI()/180)" \
               "*POW(SIN((%s*PI()/180-longitude*PI()/180)/2),2)))*1000) " \
              "AS distance FROM snapshot_mirror ORDER BY distance LIMIT 10) s " \
              "WHERE  distance < 500"
        return self.raw(sql, [lat, lat, lon])


class Mirror(models.Model):
    """ OLD Model is sucks. """
    title = models.CharField(_('Title'), max_length=200, blank=True)
    owner = models.ForeignKey(Visitor, null=True,
                              verbose_name=_('Mirror`s owner'),
                              help_text=_('Mirror`s last user'))
    location = models.CharField(_('Location'), max_length=200, blank=True)
    latitude = models.DecimalField(_('Latitude'), max_digits=19,
                                   decimal_places=10)
    longitude = models.DecimalField(_('Longitude'), max_digits=19,
                                    decimal_places=10)
    # Formerly known as device_tokens
    token = models.CharField(_('Device tokens'), max_length=200, unique=True)
    create_date = models.DateTimeField(_('Date created'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date modified'), auto_now=True)
    lock_date = models.DateTimeField(_('Date locked'), default=timezone.now)
    is_locked = models.BooleanField(_('Locked'), default=False)
    # Formerly online_time
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
    path_photo = UploadPath('snapshot/photo', None, *('visitor',))
    path_thumb = UploadPath('snapshot/photo/thumbs', None, 'thumb',
                            *('visitor',))
    path_crop = UploadPath('snapshot/photo/crops', None, 'crop',
                            *('visitor',))
    visitor = models.ForeignKey(Visitor, verbose_name=_('Photo owner'))
    mirror = models.ForeignKey(Mirror, verbose_name=_('Mirror'), blank=True,
                               null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('Title'), max_length=200, blank=True)
    photo = models.ImageField(_('Photo'), upload_to=path_photo,
                              null=True, blank=True,
                              validators=[SizeValidator(2)])
    thumb = models.ImageField(_('Thumbnail'), upload_to=path_thumb,
                              null=True, blank=True)
    description = models.TextField(_('Description'), null=True,
                                   blank=True, max_length=5000)
    create_date = models.DateTimeField(_('Date created'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date modified'), auto_now=True)
    group = models.ForeignKey('snapshot.Group', on_delete=models.SET_NULL,
                              null=True, blank=True)
    crop = models.ImageField(_('Cropped photo'), upload_to=path_crop,
                              null=True, blank=True)

    def __unicode__(self):
        return '{}: {}'.format(self.visitor, self.pk)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
        ordering = ('create_date', 'pk')


class Comment(models.Model):
    photo = models.ForeignKey(Photo, verbose_name=_('Photo'),
                              on_delete=models.CASCADE)
    author = models.ForeignKey(Visitor, verbose_name=_('Author'))
    message = models.CharField(_('Message'), max_length=160)
    create_date = models.DateTimeField(_('Date created'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date modified'), auto_now=True)

    def __unicode__(self):

        return '{}:{}:{}'.format(self.photo, self.id, self.author)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('create_date', 'pk')


class Group(models.Model):
    """ This model represents visitor`s [virtual] wardrobe. """
    # TODO: who can own the group? Only weixin user or any kind too?
    path_avatar = UploadPath('snapshot/group', 'title', '', *('owner',))
    path_thumb = UploadPath('snapshot/group/thumbs', 'title',
                            'thumb', *('owner',))
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), max_length=5000,
                                   blank=True)
    is_private = models.BooleanField(_('Private'), default=False)
    create_date = models.DateTimeField(_('Date created'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date modified'), auto_now=True)
    avatar = models.ImageField(_('Group avatar'), upload_to=path_avatar,
                               null=True, blank=True,
                               validators=[SizeValidator(2)])
    thumb = models.ImageField(_('Thumbnail'), upload_to=path_thumb,
                              null=True, blank=True)
    owner = models.ForeignKey(Visitor, verbose_name=_('Group owner'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        ordering = ('create_date', 'pk',)


class Member(models.Model):
    """ Representation of a group member.
    It not uses directly ManyToMany Relation. It is realized explicitly """
    group = models.ForeignKey(Group, verbose_name=_('Group'))
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor'))

    def __unicode__(self):
        return '{}, {}'.format(self.group, self.visitor)

    class Meta:
        verbose_name = _('Collaborator')
        verbose_name_plural = _('Collaborators')
        ordering = ('pk',)


class Tag(models.Model):
    """ Representation of tag for group """
    title = models.CharField(_('Title'), max_length=200, blank=True)
    group = models.ForeignKey(Group, verbose_name=_('Group'))
    visitor = models.ForeignKey(Visitor, verbose_name=_('Visitor'))

    def __unicode__(self):
        return '{}, {}'.format(self.group_id, self.title)

    class Meta:
        verbose_name = _('Group tag')
        verbose_name_plural = _('Group tags')
        ordering = ('pk',)
