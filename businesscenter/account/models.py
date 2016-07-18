from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from utils.validators import SizeValidator
# Create your models here.


class Vendor(models.Model):
    # TODO: Fix auto creation with empty params
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

    avatar = models.ImageField(_('Avatar'), upload_to='vendors',
                               null=True, blank=True,
                               validators=[SizeValidator(0.5)])
    thumb = models.ImageField(_('Thumbnail'),
                              upload_to='vendors/thumbs',
                              null=True, blank=True)

    def __unicode__(self):
        return self.user.username

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
        return '{},{}'.format(self.state, self.title)


class District(AbsLocation):

    city = models.ForeignKey(City, verbose_name=_('City'))

    class Meta:
        verbose_name = _('Districts')
        verbose_name_plural = _('Districts')

    def __unicode__(self):
        return '{},{}'.format(self.city, self.title)


class Store(models.Model):

    district = models.ForeignKey(District, verbose_name=_('District'))
    street = models.CharField(_('Street'), max_length=100)
    street_no = models.CharField(_('Street number'), max_length=100)
    build_name = models.CharField(_('Building name'), max_length=50,
                                  blank=True)
    build_no = models.CharField(_('Building number'), max_length=5)
    apt = models.CharField(_('Apartments'), max_length=5)
    brand_name = models.CharField(_('Brand name'), max_length=50, unique=True)
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE,
                                 verbose_name=_('Owner'), primary_key=True)
    crop = models.ImageField(_('Crop'), upload_to='stores/crops',
                             null=True, blank=True)
    photo = models.ImageField(_('Logo'), upload_to='stores',
                              blank=True, null=True)

    def get_location(self):
        return '{},{}{}{}{}{}'.format(self.district, self.street,
                                      self.street_no, self.build_name,
                                      self.build_no, self.apt)

    def __unicode__(self):
        return self.brand_name
