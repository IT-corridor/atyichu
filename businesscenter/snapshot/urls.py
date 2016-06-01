from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

snapshot_router = DefaultRouter()

snapshot_router.register(r'mirror', views.MirrorViewSet, 'mirror')
snapshot_router.register(r'photo', views.PhotoViewSet, 'photo')

urlpatterns = [
    url(r'^app/$', views.index, name='index'),
    url(r'^signature/$', views.get_signature, name='signature'),
]

urlpatterns += snapshot_router.urls
