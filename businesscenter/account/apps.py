from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = _('Account')

    def ready(self):
        from django.db.models.signals import pre_delete, post_save, post_migrate
        from .receivers import cleanup_files, add_to_vendor_group, create_vendor_group

        Vendor = self.get_model('Vendor')
        Store = self.get_model('Store')
        post_migrate.connect(create_vendor_group, sender=self)
        pre_delete.connect(cleanup_files, sender=Vendor)
        pre_delete.connect(cleanup_files, sender=Store)
        post_save.connect(add_to_vendor_group, sender=Vendor)

