from __future__ import unicode_literals

from django.contrib import admin

from . import models
from vendor_admin.admin import site


class StockInline(admin.TabularInline):
    model = models.Stock
    extra = 0
    # exclude = ()


class GalleryInline(admin.TabularInline):
    model = models.Gallery
    extra = 0


class CommodityAdmin(admin.ModelAdmin):
    # TODO: Optimize queries

    list_display = ('title', 'brand', 'kind', 'season', 'year', 'store')
    list_filter = ('brand', 'kind', 'season', 'year', 'store')
    inlines = (StockInline, GalleryInline)


admin.site.register(models.Category)
admin.site.register(models.Kind)
admin.site.register(models.Brand)
admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.Commodity, CommodityAdmin)


site.register(models.Category)
site.register(models.Kind)
site.register(models.Brand)
site.register(models.Color)
site.register(models.Size)
site.register(models.Commodity, CommodityAdmin)
