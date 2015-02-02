"""
Settings for local development.

These settings are not fast or efficient, but allow local servers to be run
using the django-admin.py utility.

This file should be excluded from version control to keep the settings local.
"""

import os.path

from production import BASE_DIR


# Run in debug mode.

DEBUG = True

TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

# Serve files locally for development.
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

STATICFILES_STORAGE = "require.storage.OptimizedCachedStaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_SERVE = True

# Use local server.

SITE_DOMAIN = "localhost:8000"

PREPEND_WWW = False

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Disable the template cache for development.

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'database.db'),
    }
}
