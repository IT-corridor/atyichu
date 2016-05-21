from __future__ import unicode_literals

from django.conf.urls import url
from django.views.decorators.cache import cache_page
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

catalog_router = DefaultRouter()
catalog_router.register(r'categories', views.CategoryViewSet, 'category')
catalog_router.register(r'kinds', views.KindViewSet, 'kind')
catalog_router.register(r'brands', views.BrandViewSet, 'brand')
catalog_router.register(r'colors', views.ColorViewSet, 'color')
catalog_router.register(r'commodities', views.CommodityViewSet, 'commodity')
catalog_router.register(r'stocks', views.StockViewSet, 'stock')
catalog_router.register(r'galleries', views.GalleryViewSet, 'gallery')


urlpatterns = catalog_router.urls

