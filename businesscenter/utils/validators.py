from __future__ import unicode_literals

from django.core.validators import BaseValidator, RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class SizeValidator(BaseValidator):
    compare = lambda self, a, b: a > b * 1024 * 1024
    clean = lambda self, x: x.size
    message = _('Max file size is %(limit_value)s MB.')
    code = 'file_size_value'


def validate_weixin(value):
    error = _('Enter a valid weixin id. This value may contain only '
              'English and Chinese letters, numbers and -, _ characters.')
    validator = RegexValidator(u'^[\w\d\-\u2E80-\u9FFF]+$', error)
    return validator(value)
