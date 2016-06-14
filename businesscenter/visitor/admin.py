from __future__ import unicode_literals
from django.contrib import admin
from . import models
# Register your models here.


class VisitorAdmin(admin.ModelAdmin):

    list_display = ('user', 'is_expired')

admin.site.register(models.Visitor, VisitorAdmin)
