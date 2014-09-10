from django.conf.urls import patterns, url
from home import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # /1/
    url(r'^(?P<week_number>\d+)/$', views.index, name='index'),
)