import dj_database_url

from decouple import config

from .base import *
from donjo.urls import urlpatterns


DEBUG = False

ALLOWED_HOSTS = ['*']

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware ',
]

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
