from __future__ import unicode_literals

from django.contrib import admin
from . import models


class PhotoInline(admin.TabularInline):
    model = models.Photo
    extra = 0


class MirrorAdmin(admin.ModelAdmin):

    list_display = ('title', 'is_locked', 'last_login')
    inlines = (PhotoInline,)

admin.site.register(models.Mirror, MirrorAdmin)
admin.site.register(models.Photo)
