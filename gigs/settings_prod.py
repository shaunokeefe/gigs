from gigs.settings_base import *

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = ()

INSTALLED_APPS += (
    'gunicorn',
)
