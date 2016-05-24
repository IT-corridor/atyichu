from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save
from .validators import SizeValidator
from utils import utils, receivers


class AbsCategory(models.Model):
    """ Each record of ref. model has its own title and priority for sorting"""
    title = models.CharField(_('Title'), max_length=50)
    priority = models.PositiveSmallIntegerField(_('Priority'), default=0)
    store = models.ForeignKey('account.Store', verbose_name=_('Store'))

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title


class Category(AbsCategory):
    """ AKA CATALOG 1 """
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('priority', )


class Kind(AbsCategory):
    """ AKA CATALOG 2 """
    category = models.ForeignKey(Category, verbose_name=_('Category'))

    class Meta:
        verbose_name = _('Kind')
        verbose_name_plural = _('Kinds')
        ordering = ('priority',)


class Brand(AbsCategory):

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ('priority',)


class Color(AbsCategory):
    html = models.CharField(_('Html code'), max_length=7)

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')
        ordering = ('priority',)


class Size(AbsCategory):

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')
        ordering = ('priority',)


class Commodity(models.Model):
    """ Basic Commodity """
    SEASONS = (
        ('0', _('Winter')),
        ('1', _('Spring')),
        ('2', _('Summer')),
        ('3', _('Autumn')),
    )
    title = models.CharField(_('Title'), max_length=100, blank=True)
    year = models.CharField(_('Year'), max_length=4)
    season = models.CharField(_('Season'), choices=SEASONS, max_length=1)
    kind = models.ForeignKey(Kind, verbose_name=_('Kind'))
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'))
    store = models.ForeignKey('account.Store', verbose_name=_('Store'))
    add_date = models.DateTimeField(_('Date added'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date modified'), auto_now=True)

    def __unicode__(self):
        # TITLE OR BRAND:KIND:YEAR
        return self.title if self.title else\
            '{}+{}+{}'.format(self.brand, self.kind, self.year)

    class Meta:
        verbose_name = _('Commodity')
        verbose_name_plural = _('Commodities')
        ordering = ('id',)


class Stock(models.Model):

    """ Nested Commodity, based on Commodity """
    # TODO: Find out what is RFID code and implement it
    # TODO: tags ArrayField or new Table
    title = models.CharField(_('Title'), max_length=100, blank=True)
    commodity = models.ForeignKey(Commodity, verbose_name=_('Commodity'),
                                  on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name=_('Color'))
    size = models.ForeignKey(Size, verbose_name=_('Size'))

    def __unicode__(self):
        # BRAND+COLOR+KIND+SIZE+YEAR
        return self.title if self.title else \
            '{}+{}+{}'.format(self.brand, self.color, self.commodity.kind,
                              self.size, self.commodity.year)

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
        unique_together = ('commodity', 'color', 'size')
        ordering = ('id',)


class Gallery(models.Model):
    # TODO: add a count constraint for the commodity equal 5

    path_photo = utils.UploadPath('gallery', 'commodity')
    path_thumb = utils.UploadPath('gallery/thumbs', 'commodity', suff='thumb')

    commodity = models.ForeignKey(Commodity, verbose_name=_('Commodity'))
    photo = models.ImageField(_('Photo'), upload_to=path_photo,
                              validators=[SizeValidator(2)])
    thumb = models.ImageField(_('Thumbnail'), upload_to=path_thumb)

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Gallery')
        ordering = ('id',)


class Tags(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    commodity = models.ForeignKey(Commodity, verbose_name=_('Commodity'))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('id',)
