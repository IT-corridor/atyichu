from __future__ import unicode_literals

from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'^$', views.index_, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^openid$', views.openid_, name='openid'),
    url(r'^dummy/$', views.dummy_api, name='dummy'),
)


