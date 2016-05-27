from __future__ import unicode_literals

import string
import random
import re


# IT LOOKS LIKE BOTH FUNCTIONS ARE USELESS
def generate_number_random(count):
    return ''.join(random.choice(string.digits) for _ in range(count))


def is_mobile(mobile):
    if re.match('^(1[34578]\d{9})$', mobile.strip()) is None:
        return False
    return True
