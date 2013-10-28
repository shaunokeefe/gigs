from gigs.settings_base import *

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = ()

INSTALLED_APPS += (
    'gunicorn',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'OPTIONS':{
        'read_default_file':'/etc/tugg/my.cnf',
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
         },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tugg/tugg.log',
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 5,
            'formatter':'standard',
            },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tugg/tugg_request.log',
            'maxBytes': 1024*1024*50, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}

ALLOWED_HOSTS = []
