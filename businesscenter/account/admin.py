from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from . import models


class VendorInline(admin.StackedInline):
    model = models.Vendor
    extra = 0


class AdminVendor(UserAdmin):

    list_display = ('first_name', 'username', 'email')
    inlines = VendorInline,


class AdminStore(admin.ModelAdmin):

    list_display = ('brand_name', 'district')
    list_filter = ('district',)
    list_select_related = ('district__city__state',)

admin.site.unregister(User)
admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.District)
admin.site.register(models.Store, AdminStore)
admin.site.register(models.Vendor)
admin.site.register(User, AdminVendor)
