from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from .validators import validate_weixin
from utils.validators import SizeValidator


class Visitor(models.Model):
    weixin = models.CharField(_('Weixin id'), max_length=30,
                              validators=[validate_weixin], unique=True,
                              help_text=_('4-30 characters, '
                                          'Chinese and English letters,'
                                          ' numbers, -, _'))
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE,
                                primary_key=True)
    avatar = models.ImageField(_('Avatar'), upload_to='visitors',
                               null=True, blank=True,
                               validators=[SizeValidator(0.5)])
    thumb = models.ImageField(_('Thumbnail'),
                              upload_to='visitors/thumbs',
                              null=True, blank=True)

    def __unicode__(self):
        return self.weixin

    class Meta:
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')
