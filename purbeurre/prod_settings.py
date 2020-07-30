import os
import dj_database_url

from purbeurre.settings import *


# debug 
DEBUG = False
TEMPLATE_DEBUG = False

# disable django debug tool bar 
INTERNAL_IPS = []

# security
ALLOWED_HOSTS = ['purbeurre-jmlm74.herokuapp.com', ]
SECRET_KEY = get_env_variable('SECRET_KEY', '')

# postgres database
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# white noise for static files
MIDDLEWARE += [ 'whitenoise.middleware.WhiteNoiseMiddleware' ]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'