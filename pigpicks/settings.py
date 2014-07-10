
"""
Django settings for pigpicks project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

SECRET_KEY = os.environ['PIGPICKS_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '.pigpicksfive.com', # Allow domain and subdomains
    '.pigpicksfive.com.', # Also allow FQDN and subdomains
]

# Templates path
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'login',
    'home',
    'rules',
    'picks',
    'league'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pigpicks.urls'

WSGI_APPLICATION = 'pigpicks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ben_pigpicks',
        'USER': 'ben',
        'PASSWORD': os.environ['PIGPICKS_MYSQL_PW'],
        'HOST': '127.0.0.1'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/projects/pigpicks/pigpicks/pigpicks/static/'


# Static files paths
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static')
),

# tinymce settings
TINYMCE_JS_URL = os.path.join(STATIC_URL, "admin/js/tinymce/tinymce.min.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, "admin/js/tinymce/")
TINYMCE_DEFAULT_CONFIG = {
    'theme': "modern"
}

# session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_AGE = 120 * 60

# email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'benlefebvre33@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['PIGPICKS_GMAIL_PW']
EMAIL_PORT = 587
