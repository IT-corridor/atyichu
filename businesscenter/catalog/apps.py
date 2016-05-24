from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CatalogConfig(AppConfig):
    name = 'catalog'
    verbose_name = _('Catalog')

    def ready(self):
        from django.db.models.signals import pre_delete, post_save, post_migrate
        from utils import utils, receivers
        from .receivers import add_vendor_catalog_perms
        # TODO: maybe it is not necessary to add here permission

        Gallery = self.get_model('Gallery')
        post_migrate.connect(receiver=add_vendor_catalog_perms,sender=self)
        pre_delete.connect(receivers.cleanup_files, sender=Gallery)
        post_save.connect(receivers.create_thumb, sender=Gallery)
