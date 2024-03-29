# -*- coding: utf-8 -*-
"""
Production Configurations
"""
from __future__ import absolute_import, unicode_literals

from unipath import Path
import dj_database_url

import logging
import environ, os

from .base import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY_PROD', default='')
DEBUG=False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'autentica.lib.error_handler.HandleBusinessExceptionMiddleware'
]


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
#SECURE_HSTS_SECONDS = 60
#SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
#    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
#SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
#    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
#SECURE_BROWSER_XSS_FILTER = True
#SESSION_COOKIE_SECURE = True
#SESSION_COOKIE_HTTPONLY = True
#SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
#CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_HTTPONLY = True
#X_FRAME_OPTIONS = 'DENY'

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*', ])
# END SITE CONFIGURATION

INSTALLED_APPS += ['gunicorn', ]

STATIC_ROOT = '/var/www/html/votacao/static'

MEDIA_ROOT = '/var/www/html/votacao/media'


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
#INSTALLED_APPS += ['storages', ]

#AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
#AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
#AWS_AUTO_CREATE_BUCKET = True
#AWS_QUERYSTRING_AUTH = False
#AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

# AWS cache settings, don't change unless you know what you're doing:
#AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
#AWS_HEADERS = {
#    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
#        AWS_EXPIRY, AWS_EXPIRY))
#}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.

#  See:http://stackoverflow.com/questions/10390244/
#from storages.backends.s3boto import S3BotoStorage
#StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
#MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')
#DEFAULT_FILE_STORAGE = 'config.settings.production.MediaRootS3BotoStorage'

#MEDIA_URL = 'https://s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME

# Static Assets
# ------------------------

#STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
#STATICFILES_STORAGE = 'config.settings.production.StaticRootS3BotoStorage'
# See: https://github.com/antonagestam/collectfast
# For Django 1.7+, 'collectfast' should come before
# 'django.contrib.staticfiles'
#AWS_PRELOAD_METADATA = True
#INSTALLED_APPS = ['collectfast', ] + INSTALLED_APPS

# EMAIL
# ------------------------------------------------------------------------------
#DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
#                         default='Ramais <noreply@example.com>')
#EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Ramais CMC]')
#SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
#INSTALLED_APPS += ['anymail', ]
#ANYMAIL = {
#    'MAILGUN_API_KEY': env('DJANGO_MAILGUN_API_KEY'),
#    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_SENDER_DOMAIN')
#}
#EMAIL_BACKEND = 'anymail.backends.mailgun.MailgunBackend'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# Use the Heroku-style specification
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
#DATABASES['default'] = env.db('DATABASE_URL')
#DATABASES = {
#    'ldap': {
#        'ENGINE': 'ldapdb.backends.ldap',
#        'NAME': env('LDAP_AUTH_URL'),
#     },
#    'default': env.db(),
#}

# CACHING
# ------------------------------------------------------------------------------
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#        'TIMEOUT': 60,
#        'KEY_PREFIX': 'djcache',
#    }
#}

#CACHES = {
#    'default': {
#        'BACKEND': 'django_redis.cache.RedisCache',
#        'LOCATION': '/var/run/redis/redis.sock',
#        'OPTIONS': {
#            'DB': 1,
#            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#            'IGNORE_EXCEPTIONS': True
#        }
#    }
# }


# Sentry Configuration
#SENTRY_DSN = env('DJANGO_SENTRY_DSN')
#SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
        "file" : {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "file" : {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "votacao.log",
            "formatter": "file",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",  
            "propagate": True,
        },
         'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",  
            "propagate": True,
        },
    },
}


#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': True,
#    'root': {
#        'level': 'WARNING',
#        'handlers': ['sentry', ],
#    },
#    'formatters': {
#        'verbose': {
#            'format': '%(levelname)s %(asctime)s %(module)s '
#                      '%(process)d %(thread)d %(message)s'
#        },
#    },
#    'handlers': {
#        'sentry': {
#            'level': 'ERROR',
#            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
#        },
#        'console': {
#            'level': 'DEBUG',
#            'class': 'logging.StreamHandler',
#            'formatter': 'verbose'
#        },
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'filename': 'votacao.log',
#        },

#    },
#    'loggers': {
#        'django.db.backends': {
#            'level': 'ERROR',
#            'handlers': ['console', ],
#            'propagate': False,
#        },
#        'raven': {
#            'level': 'DEBUG',
#            'handlers': ['console', ],
#            'propagate': False,
#        },
#        'sentry.errors': {
#            'level': 'DEBUG',
#            'handlers': ['console', ],
#            'propagate': False,
#        },
#        'django.security.DisallowedHost': {
#            'level': 'ERROR',
#            'handlers': ['console', ],
#            'propagate': False,
#        },

#        'votacao': {
#            'level': 'INFO',
#            'handlers': ['console', 'file'],
            # required to avoid double logging with root logger
#            'propagate': False,
#        },
#        'django': {
#            'handlers': ['file'],
#            'level': 'DEBUG',
#            'propagate': True,
#        },
#    },
#}
#SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
#RAVEN_CONFIG = {
#    'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
#    'DSN': SENTRY_DSN
#}

# Custom Admin URL, use {% url 'admin:index' %}
#ADMIN_URL = env('DJANGO_ADMIN_URL')

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

#CELERY_ACCEPT_CONTENT = ['json']

CRONJOBS = [
   ('00 00 * * *', 'votacao.cron.jobs.fecha_votacoes')
]