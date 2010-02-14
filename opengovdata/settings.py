# -*- coding: utf8 -*-
# Django settings for opengovdata project.
import os
DEBUG = False
#DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    ('Ivan Begtin', 'ibegtin@gmail.com'),
)

MANAGERS = ADMINS

#DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_ENGINE = 'mysql'
#DATABASE_NAME = '/var/www/opengovdata.ru/opengovdata/db.db'             # Or path to database file if using sqlite3.
DATABASE_NAME = 'opengovdata'
DATABASE_USER = 'opengovdata'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/opengovdata.ru/html/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

ROOT_URLCONF = 'opengovdata.urls'


#SECRET_KEY = 'a1wyygkm7g&6u3xx47ohe&4yh^47w39wr0$73jq9_y*59-=mt&'
SECRET_KEY = 'very_secret_key_for_opengovdata.ru_with_$and&'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
#    'django_authopenid.context_processors.authopenid',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
#    'django_authopenid.middleware.OpenIDMiddleware',
)

ROOT_URLCONF = 'opengovdata.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

#LOGIN_REDIRECT_URL = '/'
ugettext = lambda s: s
#LOGIN_URL = '/%s%s' % (ugettext('account/'), ugettext('signin/'))
#LOGIN_REDIRECT_URL = LOGIN_URL
ACCOUNT_ACTIVATION_DAYS = 10

INSTALLED_APPS = (
    'djlinks',
    'opendata',
    'normdocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'registration',
#    'django_authopenid',
)

SITE_MAIN_MENU = [
    {'code' : 'home', 'name' : u'Главная', 'url' : '/'},
    {'code' : 'news', 'name' : u'Новости', 'url' : '/news/'},
    {'code' : 'sources', 'name' : u'Источники информации', 'url' : '/sources/'},
    {'code' : 'opendata', 'name' : u'Открытые данные', 'url' : '/opendata/'},
    {'code' : 'laws', 'name' : u'Банк документов', 'url' : '/laws/', 'last' : True},
]
        