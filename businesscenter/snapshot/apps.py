from __future__ import unicode_literals

from django.apps import AppConfig


class SnapshotConfig(AppConfig):
    name = 'snapshot'

    def ready(self):
        from django.db.models.signals import pre_delete, post_save
        from utils import receivers

        Photo = self.get_model('Photo')
        Group = self.get_model('Group')
        pre_delete.connect(receivers.cleanup_files_photo, sender=Photo)
        pre_delete.connect(receivers.cleanup_files_avatar, sender=Group)

        post_save.connect(receivers.create_thumb_photo_320, sender=Photo)
        post_save.connect(receivers.create_thumb_avatar_320, sender=Group)
