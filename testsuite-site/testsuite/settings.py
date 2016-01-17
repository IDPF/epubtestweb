# Django settings for testsuite project.
import os

# all locally-overridable stuff goes here
DEBUG = False
template_debug = False
db_file = '/home/djangoweb/epubtestweb-db/testsuite.db'
template_dir = '/home/djangoweb/epubtestweb/testsuite-site/templates'
media_root = '/home/djangoweb/epubtestweb/testsuite-site/media'
media_url = '/media/'
static_url = '/static/'
static_root = '/home/djangoweb/epubtestweb/testsuite-site/static'
epub_downloads_root = '/home/djangoweb/epub-testsuite/build'
epub_downloads_url = '/epubs/' #symlinked to epub_downloads_root
previous_db = '/home/djangoweb/epubtestweb-db/testsuite-demo.db'
secret_key = 'utq699x(arx2auy=fnmotm^_7g2d^fa4n+kefz%fev1)noiv1e' # change or override this
allowed_hosts = [] 
enable_analytics = True
allow_robots = True
readonly = False # disable pages that require a login
# end of overrides

try:
    from .local_settings import *
except ImportError:
    pass

MEDIA_ROOT = media_root
MEDIA_URL = media_url

STATIC_ROOT = static_root
STATIC_URL = static_url

EPUB_ROOT = epub_downloads_root
EPUB_URL = epub_downloads_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = secret_key

ALLOWED_HOSTS = allowed_hosts

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testsuite_app',
    'analytical',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'testsuite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [template_dir,],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': template_debug
        },

    },
]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': db_file,                        # Or path to database file if using sqlite3.
    },

    'previous': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': previous_db,                      
    },
}

SITE_ID = 1

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'testsuite.wsgi.application'

AUTH_USER_MODEL = 'testsuite_app.UserProfile'
LOGIN_REDIRECT_URL = '/manage/'


GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-47689191-1'
GOOGLE_ANALYTICS_SITE_SPEED = True
GOOGLE_ANALYTICS_INTERNAL_IPS = '142.136.168.189'
GOOGLE_ANALYTICS_ANONYMIZE_IP = True





