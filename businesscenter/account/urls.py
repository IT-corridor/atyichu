from django.conf.urls import url
from django.views.decorators.cache import cache_page
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

store_router = DefaultRouter()
store_router.register(r'stores', views.StoreViewSet, 'stores')


urlpatterns = (
    url(r'^states/$', cache_page(300)(views.StateView.as_view()),
        name='state-list'),
    url(r'^cities/$', cache_page(300)(views.CityView.as_view()),
        name='city-list'),
    url(r'^districts/$', cache_page(300)(views.District.as_view()),
        name='district-list'),
    url(r'^users/$', views.ProfileListCreateView.as_view(),
        name='profile-list'),
    url(r'^users/(?P<pk>\d+)/$',
        views.ProfileRetrieveUpdateView.as_view(), name='profile-detail'),
    url(r'^users/(?P<pk>\d+)/password/$',
        views.ProfilePasswordUpdatedView.as_view(), name='profile-password'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += store_router.urls

