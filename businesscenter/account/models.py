from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save
from receivers import cleanup_files, add_to_vendor_group
# Create your models here.


class AbsLocation(models.Model):
    title = models.CharField(_('Title'), db_index=True, max_length=100)

    class Meta:
        abstract = True


class State(AbsLocation):

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ('id',)

    def __unicode__(self):
        return self.title


class City(AbsLocation):
    state = models.ForeignKey(State, verbose_name=_('State'))

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __unicode__(self):
        return '{}:{}'.format(self.state, self.title)


class District(AbsLocation):

    city = models.ForeignKey(City, verbose_name=_('City'))

    class Meta:
        verbose_name = _('Districts')
        verbose_name_plural = _('Districts')

    def __unicode__(self):
        return '{}:{}'.format(self.city, self.title)


class Store(models.Model):

    logo = models.ImageField(_('Logo'), upload_to='stores',
                             blank=True, null=True)
    district = models.ForeignKey(District, verbose_name=_('District'))
    street = models.CharField(_('Street'), max_length=100)
    build_name = models.CharField(_('Building name'), max_length=50)
    build_no = models.CharField(_('Building number'), max_length=5)
    apt = models.CharField(_('Apartments'), max_length=5)
    brand = models.CharField(_('Brand'), max_length=50)

    def get_location(self):
        return '{}:{}:{}:{}:{}'.format(self.district, self.street,
                                       self.build_name, self.build_no,
                                       self.apt)

    def __unicode__(self):
        return self.brand


class Vendor(User):
    # TODO: Replace store relation to store model (One-to-One field)
    # What with the store?
    # TODO: Add something to identify that it is
    # a vendor and not a regular user

    avatar = models.ImageField(_('Avatar'), upload_to='vendors',
                               null=True, blank=True)
    store = models.ForeignKey(Store, verbose_name=_('Store'),
                              null=True, blank=True)

    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')

pre_delete.connect(cleanup_files, sender=Vendor)
pre_delete.connect(cleanup_files, sender=Store)
post_save.connect(add_to_vendor_group, sender=Vendor)
