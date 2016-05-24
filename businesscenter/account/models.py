from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Vendor(User):
    avatar = models.ImageField(_('Avatar'), upload_to='vendors',
                               null=True, blank=True)

    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')


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
    brand_name = models.CharField(_('Brand name'), max_length=50)
    owner = models.OneToOneField(Vendor, on_delete=models.CASCADE,
                                 verbose_name=_('Owner'))

    def get_location(self):
        return '{}:{}:{}:{}:{}'.format(self.district, self.street,
                                       self.build_name, self.build_no,
                                       self.apt)

    def __unicode__(self):
        return self.brand_name

