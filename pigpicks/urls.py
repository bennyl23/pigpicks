from django.conf.urls import patterns, include, url
from django.contrib import admin
from pigpicks import settings


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^picks/', include('picks.urls', namespace='picks')),
    url(r'^league/', include('league.urls', namespace='league')),
    url(r'^rules/', include('rules.urls', namespace='rules')),
)
