from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.validators import SizeValidator
from utils import utils, receivers


class AbsCategory(models.Model):
    """ Each record of ref. model has its own title and priority for sorting"""
    title = models.CharField(_('Title'), max_length=50)
    priority = models.PositiveSmallIntegerField(_('Priority'), default=0)


    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title


class AbsStoreCategory(AbsCategory):
    store = models.ForeignKey('account.Store', verbose_name=_('Store'))

    class Meta:
        abstract = True


class Category(AbsCategory):
    """ AKA CATALOG 1. Can be set only by the administrator of the platform."""

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('priority', 'pk')


class Kind(AbsCategory):
    """ AKA CATALOG 2.
    Can be set only by the administrator of the platform. """
    category = models.ForeignKey(Category, verbose_name=_('Category'))

    class Meta:
        verbose_name = _('Kind')
        verbose_name_plural = _('Kinds')
        ordering = ('priority', 'pk')


class Brand(AbsStoreCategory):

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ('priority', 'pk')


class Color(AbsStoreCategory):
    html = models.CharField(_('Html code'), max_length=7, blank=True)

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')
        ordering = ('priority', 'pk')


class Size(AbsCategory):

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')
        ordering = ('priority', 'pk')


class Commodity(models.Model):
    """ Basic Commodity. Because of RFID,
    we need to create each time a new instance of commodity,
    even if they differ only by color or size."""
    SEASONS = (
        ('0', _('Winter')),
        ('1', _('Spring')),
        ('2', _('Summer')),
        ('3', _('Autumn')),
    )
    title = models.CharField(_('Title'), max_length=100, blank=True)
    year = models.CharField(_('Year'), max_length=4)
    season = models.CharField(_('Season'), choices=SEASONS, max_length=1)
    add_date = models.DateTimeField(_('Date added'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date modified'), auto_now=True)
    kind = models.ForeignKey(Kind, verbose_name=_('Kind'))
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'))
    color = models.ForeignKey(Color, verbose_name=_('Color'))
    size = models.ForeignKey(Size, verbose_name=_('Size'))
    store = models.ForeignKey('account.Store', verbose_name=_('Store'))

    def __unicode__(self):
        # BRAND+COLOR+KIND+SIZE+YEAR
        return self.title if self.title else \
            '{}+{}+{}'.format(self.brand, self.color, self.kind,
                              self.size, self.year)

    class Meta:
        verbose_name = _('Commodity')
        verbose_name_plural = _('Commodities')
        ordering = ('id',)


class Gallery(models.Model):
    # TODO: add a count constraint for the commodity equal 5
    # TODO: make it with viewset in the perform_create

    path_photo = utils.UploadPath('gallery', 'commodity')
    path_thumb = utils.UploadPath('gallery/thumbs', 'commodity', suff='thumb')

    commodity = models.ForeignKey(Commodity, verbose_name=_('Commodity'))
    photo = models.ImageField(_('Photo'), upload_to=path_photo,
                              validators=[SizeValidator(2)])
    thumb = models.ImageField(_('Thumbnail'), upload_to=path_thumb,
                              null=True, blank=True)

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Gallery')
        ordering = ('id',)


class Tag(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    commodity = models.ForeignKey(Commodity, verbose_name=_('Commodity'))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('id',)
