from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

snapshot_router = DefaultRouter()

snapshot_router.register(r'mirror', views.MirrorViewSet, 'mirror')
snapshot_router.register(r'photo', views.PhotoViewSet, 'photo')
snapshot_router.register(r'comment', views.CommentViewSet, 'comment')
snapshot_router.register(r'tag', views.TagViewSet, 'tag')
snapshot_router.register(r'member', views.MemberViewSet, 'member')
snapshot_router.register(r'group', views.GroupViewSet, 'group')
snapshot_router.register(r'group-photo', views.GroupPhotoViewSet,
                         'photo-g')
snapshot_router.register(r'visitor', views.VisitorViewSet, 'visitor')

urlpatterns = [
    url(r'^signature/$', views.get_signature, name='signature'),
]

urlpatterns += snapshot_router.urls
