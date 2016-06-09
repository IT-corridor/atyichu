from __future__ import unicode_literals

from django.contrib import admin
from . import models


class PhotoInline(admin.TabularInline):
    model = models.Photo
    extra = 0


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


class MirrorAdmin(admin.ModelAdmin):

    list_display = ('title', 'is_locked', 'last_login')
    inlines = (PhotoInline,)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'mirror')
    inlines = (CommentInline, )


admin.site.register(models.Mirror, MirrorAdmin)
admin.site.register(models.Photo, PhotoAdmin)
admin.site.register(models.Comment)
