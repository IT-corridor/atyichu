from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from visitor.models import Visitor, VisitorExtra
from django.db.models import Q

class Command(BaseCommand):
    help = 'Moves oauth2 data to another (related) table'

    def handle(self, *args, **options):
        visitors = Visitor.objects.all()
        for data in visitors:
            VisitorExtra.objects.create(
                openid=data.weixin,
                access_token=data.access_token,
                refresh_token=data.refresh_token,
                expires_in=data.expires_in,
                token_date=data.token_date,
                visitor_id=data.pk
            )
        self.stdout.write(
            self.style.SUCCESS('OAuth2 data has been moved!'))
