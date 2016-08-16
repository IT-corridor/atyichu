from __future__ import unicode_literals
from django.contrib import admin
from . import models
# Register your models here.


class VisitorAdmin(admin.ModelAdmin):

    list_display = ('user',)
    readonly_fields = ('unionid',)


class VisitorExtraAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'is_expired')
    readonly_fields = ('openid', 'access_token', 'refresh_token',
                       'expires_in', 'token_date',)

admin.site.register(models.Visitor, VisitorAdmin)
admin.site.register(models.VisitorExtra, VisitorExtraAdmin)
