from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Creates a vendor group. Run this only after migration' \
           ' of account and catalog apps.'

    def handle(self, *args, **options):
        permissions = Permission.objects.\
            filter(content_type__app_label__iexact='catalog')
        try:
            group = Group.objects.create(name='vendors')
            group.permissions.set(permissions)
        except Exception as e:
            raise CommandError('An error has been occurred: {}'.format(e))
        else:
            self.stdout.write(
                self.style.SUCCESS('Group "vendors" has been created!'))
