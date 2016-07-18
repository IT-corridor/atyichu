from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from utils.validators import validate_weixin
from utils.validators import SizeValidator


class Visitor(models.Model):
    """ This model extends basic authentication model (of Django).
    It used to authenticate user ONLY via WECHAT (WEXIN) API. """
    weixin = models.CharField(_('Weixin open id'), max_length=30,
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
    access_token = models.CharField(_('Weixin Access Token'), max_length=255)
    refresh_token = models.CharField(_('Weixin Refresh Token'), max_length=255)
    expires_in = models.PositiveIntegerField(_('Token expires in'))
    token_date = models.DateTimeField(_('Token date'), default=timezone.now)

    def is_expired(self):
        """Not a field --- it is a method. Checks if token is expired.
        Returns True or False."""
        return timezone.now() >\
               self.token_date + timezone.timedelta(seconds=self.expires_in)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')
