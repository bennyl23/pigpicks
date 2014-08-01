from django.conf.urls import patterns, url
from picks import views


urlpatterns = patterns('',
    # /picks/
    url(r'^$', views.index, name='index'),
    # /picks/1/
    url(r'^(?P<week_number>\d+)/$', views.index, name='index'),
    # /picks/bestbet/
    url(r'^bestbet/$', views.bestbet, name='bestbet'),
    # /picks/confirmation/
    url(r'^confirmation/$', views.confirmation, name='confirmation'),
)
