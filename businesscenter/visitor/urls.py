from __future__ import unicode_literals

from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^openid$', views.openid, name='openid'),
    url(r'^dummy/$', views.dummy_api, name='dummy'),
    url(r'^is_authenticated/$', views.is_authenticated, name='is_auth'),
)


