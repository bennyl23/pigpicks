from django.conf.urls import patterns, url
from login import views


urlpatterns = patterns('',
    # /login/
    url(r'^$', views.index, name='index'),
    # /login/register/
    url(r'^register/$', views.register, name='register'),
    # /login/forgot_password/
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    # /login/logout/
    url(r'^logout/$', views.logout, name='logout'),
    # /login/session_ended/
    url(r'^(?P<session_code>\w+)/$', views.index, name='index')
)