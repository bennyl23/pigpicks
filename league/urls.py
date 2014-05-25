from django.conf.urls import patterns, url
from league import views


urlpatterns = patterns('',
    # /league/
    url(r'^$', views.index, name='index'),
    # /league/1/
    url(r'^(?P<week_number>\d+)/$', views.index, name='index'),
    # /league/breakdown/
    url(r'^breakdown/$', views.breakdown, name='breakdown'),
    # /league/breakdown/1/
    url(r'^breakdown/(?P<week_number>\d+)/$', views.breakdown, name='breakdown'),
    # /league/standings/
    url(r'^standings/$', views.standings, name='standings'),
)
