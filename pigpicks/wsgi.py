"""
WSGI config for pigpicks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/pigpicks/lib/python2.6/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/projects/pigpicks/pigpicks')
sys.path.append('/projects/pigpicks/pigpicks/pigpicks')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pigpicks.settings'

# Activate your virtual env
activate_env=os.path.expanduser("~/.virtualenvs/pigpicks/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
