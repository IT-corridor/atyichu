from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from . import models


class StoreInline(admin.StackedInline):
    model = models.Store
    extra = 0


class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.Vendor


class AdminVendor(UserAdmin):

    list_display = ('first_name', 'username', 'email')
    form = ProfileChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),
    )
    inlines = StoreInline,


class AdminStore(admin.ModelAdmin):

    list_display = ('brand', 'district')
    list_filter = ('district',)
    list_select_related = ('district__city__state',)

admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.District)
admin.site.register(models.Store, AdminStore)
admin.site.register(models.Vendor, AdminVendor)
