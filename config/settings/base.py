# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import environ, os
import urllib3

urllib3.disable_warnings()

def gettext_noop(s):
    return s

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('votacao')

ALLOWED_HOSTS=['*']

# Load operating system environment variables and then prepare to use them
env = environ.Env()
env.read_env(env_file=ROOT_DIR('.env'))

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
     'pipeline',
     'djangobower',
     'crispy_forms',
     'compressor',
     'rest_framework',
     'ldapdb',
     'autentica',
     'consumer',
     'easy_pdf',
     'cmcreport',
     'django_nose',
     'django_crontab',
     'django_python3_ldap',
#     'tinymce',
#     'corsheaders',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'votacao.api.apps.ApiConfig',
    'votacao.votacao.apps.VotacaoConfig',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
'''
CORS_ORIGIN_ALLOW_ALL           = True
CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
'''

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
#    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'autentica.lib.error_handler.HandleBusinessExceptionMiddleware',
    # removido no Django 2: 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
]

# ALTERAÇÕES NO USER PARA GUARDAR INFO DO LDAP
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = 'autentica.User'

# SERVIDOR DE MICRO SERVICOS
# ------------------------------------------------------------------------------
MSCMC_SERVER = env('MSCMC_SERVER')

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', True)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""DIF""", 'you@example.com'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': env('LDAP_AUTH_URL'),
     },
    'default': env.db(),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

DATABASE_ROUTERS = ['ldapdb.router.Router']


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'
#USE_TZ=True
# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'pt-BR'

LANGUAGES = [
    ('pt-br', gettext_noop('Brazilian Portuguese')),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
#USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
    str(ROOT_DIR.path('components/bower_components')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'pipeline.finders.PipelineFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    # "django_python3_ldap.auth.LDAPBackend",
    'django.contrib.auth.backends.ModelBackend',
 ]


# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

# LOGGING
# ------------------------------------------------------------------------------

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
        "django_python3_ldap": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# PIPELINE
# ------------------------------------------------------------------------------

PIPELINE = {
    'PIPELINE_ENABLED': False,
    'JS_COMPRESSOR': False,
    'CSS_COMPRESSOR': False,
    'STYLESHEETS': {
        'master': {
            'source_filenames': (
              'bootstrap/dist/css/bootstrap.css',
              #'bootstrap-calendar/css/calendar.min.css',
              'bootstrap-datepicker/dist/css/bootstrap-datepicker3.css',
              'bootstrap-select/dist/css/bootstrap-select.css',
              'datatables/media/css/jquery.dataTables.css',
              'datatables/media/css/dataTables.bootstrap.css',
              'datatables.net-responsive-bs/css/responsive.bootstrap.min.css',
              #'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css',
              #'fullcalendar/dist/fullcalendar.min.css',
              'callout.css',
              'estilos.css',
              #'event.css',
            ),
            'output_filename': 'css/master.css',
        },
    },
    'JAVASCRIPT': {
        'master': {
            'source_filenames': (
              'jquery/jquery.js',
              'moment/min/moment.min.js',
              'moment/locale/pt-br.js',
              'bootstrap/dist/js/bootstrap.min.js',
              'underscore/underscore-min.js',
              #'bootstrap-calendar/js/language/pt-BR.js',
              #'bootstrap-calendar/js/calendar.min.js',
              'bootstrap-datepicker/dist/js/bootstrap-datepicker.js',
              'bootstrap-datepicker/dist/locales/bootstrap-datepicker.pt-BR.min.js',
              'bootstrap-select/dist/js/bootstrap-select.js',
              'fontawesome/svg-with-js/js/fontawesome-all.min.js',
              'datatables/media/js/jquery.dataTables.js',
              'datatables/media/js/dataTables.bootstrap.js',
              'datatables.net-responsive/js/dataTables.responsive.min.js',
              'datatables.net-responsive-bs/js/responsive.bootstrap.min.js',
              'datatables-datetime-moment/dist/js/datetime-moment.min.js',
              'axios/dist/axios.min.js',
              'vue/dist/vue.min.js',
              'build.js',
              #'eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
              #'fullcalendar/dist/fullcalendar.min.js',
              #'fullcalendar/dist/gcal.min.js',
              #'fullcalendar/dist/locale-all.min.js',
            ),
            'output_filename': 'js/master.js',
        }
    }
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
#STATICFILES_STORAGE = 'django_pipeline_forgiving.storages.PipelineForgivingStorage'

# BOWER
# ------------------------------------------------------------------------------

BOWER_COMPONENTS_ROOT = str(ROOT_DIR.path('components'))
BOWER_INSTALLED_APPS = (
    'jquery#1.9.1',
    #'jquery',
    'underscore',
    'bootstrap#3',
    #'bootstrap-calendar',
    #'jasny-bootstrap',
    'datatables',
    'datatables-bootstrap3',
    'bootstrap-3-datepicker',
    'bootstrap-datepicker',
    'datatables.net-responsive-bs',
    'datatables-datetime-moment',
    'bootstrap-select',
    #'eonasdan-bootstrap-datetimepicker#latest',
    #'bootstrap3-datetimepicker',
    #'vue',
    #'vue-strap',
    'fontawesome',
    'moment',
    'axios',
    'vue',
    #'fullcalendar',
    #'bootstrap-select'
)

# LDAP
# ------------------------------------------------------------------------------
#LDAP_AUTH_URL = "ldap://ldap"
LDAP_AUTH_URL = env('LDAP_AUTH_URL', default='')
LDAP_AUTH_USE_TLS = env('LDAP_AUTH_USE_TLS', default=False, cast=bool)
# LDAP_AUTH_USE_TLS = True
# LDAP_AUTH_SEARCH_BASE = env('LDAP_AUTH_SEARCH_BASE', default='')
LDAP_AUTH_SEARCH_BASE = env('LDAP_AUTH_SEARCH_BASE', default='')
LDAP_AUTH_BIND_BASE = env('LDAP_AUTH_BIND_BASE', default='')

LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

LDAP_AUTH_OBJECT_CLASS = env('LDAP_AUTH_OBJECT_CLASS', default='')
# LDAP_AUTH_OBJECT_CLASS = "organizationalPerson"
LDAP_AUTH_USER_FIELDS = {
    "username": env('LDAP_AUTH_USER_FIELDS_USERNAME', default=''),
    "first_name": env('LDAP_AUTH_USER_FIELDS_FIRST_NAME', default=''),
    "last_name": env('LDAP_AUTH_USER_FIELDS_LAST_NAME', default=''),
    "email": env('LDAP_AUTH_USER_FIELDS_EMAIL', default=''),
    #"matricula": env('LDAP_AUTH_USER_FIELDS_MATRICULA', default=''),
    #"pessoa": env('LDAP_AUTH_USER_FIELDS_PESSOA', default=''),
    "lotado": env('LDAP_AUTH_USER_FIELDS_LOTADO', default=''),
    "chefia": env('LDAP_AUTH_USER_FIELDS_CHEFIA', default=''),
    "cpf": env('LDAP_AUTH_USER_FIELDS_CPF', default=''),
}

LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"
LDAP_ALWAYS_SEARCH_BIND = True
# LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_openldap"
#AUTH_LDAP_BIND_USER = "cn=authproxy,dc=cmc,dc=pr,dc=gov,dc=br"
#AUTH_LDAP_BIND_PASSWORD = "authproxy"


# LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "dc=cmc,dc=pr,dc=gov,dc=br"
# LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "cmc.pr.gov.br"
LDAP_AUTH_CONNECTION_USERNAME = "cn=authproxy,dc=cmc,dc=pr,dc=gov,dc=br"
LDAP_AUTH_CONNECTION_PASSWORD = "authproxy"
# LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "ECDC"
# LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "cmc.pr.gov.br"

LDAP_BIND_USERNAME = env('LDAP_BIND_USERNAME', default='')
LDAP_BIND_PASSWORD = env('LDAP_BIND_PASSWORD', default='')



LDAP_AUTH_CONNECT_TIMEOUT = None
LDAP_AUTH_RECEIVE_TIMEOUT = None

#X_FRAME_OPTIONS = 'SAMEORIGIN'

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'link image preview codesample contextmenu table code lists',
    'toolbar1': 'formatselect | bold italic underline | alignleft aligncenter alignright alignjustify '
               '| bullist numlist | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'statusbar': True,
    'width': 'auto',
    'height': 360,
}

SETTINGS_EXPORT = [
    'MSCMC_SERVER',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

CRONJOBS = [
   ('01 00 * * *', 'votacao.cron.jobs.fecha_votacoes', '>> cron_jobs.log')
]