from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from snapshot.models import Photo


class Command(BaseCommand):
    help = 'Refresh secondary remakes secondary photos (thumbs, crops)'

    def handle(self, *args, **options):

        try:
            photos = Photo.objects.all()
            for photo in photos:
                photo.crop.delete(True)
                photo.thumb.delete(True)
                photo.cover.delete(True)
                photo.save()

        except Exception as e:
            raise CommandError('An error has been occurred: {}'.format(e))
        else:
            self.stdout.write(
                self.style.SUCCESS('Photos have been refreshed!'))
