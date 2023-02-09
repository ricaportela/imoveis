import os

from decouple import config, Csv
from dj_database_url import parse as dburl

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[], cast=Csv())

# Admins for Django report error
ADMINS = (("Ricardo Portela", "ricaportela@gmail.com"),)


# Application definition

INSTALLED_APPS = (
    #'flat',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_extensions",
    "test_without_migrations",
    "debug_toolbar",
    "favicon",
    "imoveisfinanciados.utils",
    "imoveisfinanciados.account",
    "imoveisfinanciados.core",
    "imoveisfinanciados.simulator",
    "imoveisfinanciados.realty",
    "imoveisfinanciados.catalog",
    "imoveisfinanciados.advertises",
)

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

CSRF_USE_SESSIONS = True

ROOT_URLCONF = "imoveisfinanciados.urls"

WSGI_APPLICATION = "imoveisfinanciados.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

default_dburl = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")

DATABASES = {
    "default": config("DATABASE_URL", default=default_dburl, cast=dburl),
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = "utf-8"

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = "."
DECIMAL_SEPARATOR = ","
NUMBER_GROUPING = 3


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = config("STATIC_URL", default="/static/")
STATIC_ROOT = config("STATIC_ROOT", default="public")

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Media files
MEDIA_URL = config("MEDIA_URL", default="media")
MEDIA_ROOT = config("MEDIA_ROOT", default=os.path.join(BASE_DIR, "uploads"))


# Template dirs
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.template.context_processors.csrf",
                "django.contrib.messages.context_processors.messages",
                "imoveisfinanciados.simulator.context_processors.search_forms",
                "imoveisfinanciados.realty.context_processors.user_state",
                "imoveisfinanciados.account.context_processors.current_user",
                "imoveisfinanciados.catalog.context_processors.has_catalog",
            ],
        },
    },
]

# Authentication
AUTH_USER_MODEL = "account.User"

# File system storage - fix ascii errors on filename
DEFAULT_FILE_STORAGE = (
    "imoveisfinanciados.utils.asciifilesystemstorage.ASCIIFileSystemStorage"
)

# Email
# https://docs.djangoproject.com/en/1.7/topics/email/#configuring-email-for-development
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
# EMAIL_PORT = config('EMAIL_PORT', default=1025)
DEFAULT_FROM_EMAIL = "naoresponda@imoveisfinanciados.com"
SERVER_EMAIL = "naoresponda@imoveisfinanciados.com"

FAVICON_PATH = STATIC_URL + "images/favicon.ico"

# https://stackoverflow.com/questions/66971594/auto-create-primary-key-used-when-not-defining-a-primary-key-type-warning-in-dja
# (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
