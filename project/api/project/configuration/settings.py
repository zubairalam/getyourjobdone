import os
from os.path import join
from configurations import values, Configuration

# for scheduling feed downloads and other asks using django-celery library
import djcelery

djcelery.setup_loader()
from celery import app as celery_app

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Authentication(object):
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend",
    )
    AUTH_USER_MODEL = 'accounts.User'
    LOGIN_REDIRECT_URL = '/accounts/dashboard'
    ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'


class Caching(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 60,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }


class Database(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'project',
            'USER': 'vagrant',
            'PASSWORD': 'vagrant',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'CONN_MAX_AGE': 60
        }
    }


class Email(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-EMAIL_BACKEND
    ADMINS = (
        ('XeonTek Ltd', 'enquiries@xeontek.com'),
    )
    # EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    EMAIL_BACKEND = 'post_office.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'developers@xeontek.com'
    EMAIL_HOST_PASSWORD = 'pythongeeks'
    DEFAULT_FROM_EMAIL = 'developers@xeontek.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    MANAGERS = ADMINS


class Fixture(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
    FIXTURE_DIRS = (join(BASE_DIR, 'fixtures'),)


class Localisation(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings
    LANGUAGE_CODE = 'en'
    TIME_ZONE = 'Europe/London'
    USE_I18N = values.BooleanValue(True)
    USE_L10N = values.BooleanValue(True)
    USE_TZ = values.BooleanValue(True)


class Logging(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': values.BooleanValue(False),
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': values.BooleanValue(True),
            },
        }
    }


class Media(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'


class Models(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#models
    # django apps
    DJANGO_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'django.contrib.webdesign',
        'django.contrib.formtools',
    )
    # third party apps
    THIRD_PARTY_APPS = (
        'constance',  # dynamic settings
        'django_extensions',  # useful extensions for django mgmt
        'djcelery',  # async
        'endless_pagination',  # pagination support
        'haystack',  # full-text search support.
        'model_utils',  # useful utils for django
        'multiselectfield',  # m2m support for choices
        'post_office',  # email sending.
        'taggit',  # tags support
        'widget_tweaks',  # modify form rendering
    )


    # social login providers
    SOCIAL_LOGIN_APPS = (
        'allauth',  # social logins
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.linkedin_oauth2',
    )

    # apps local for this project go here.
    LOCAL_APPS = (
        'configuration',
        'apps.accounts',
        'apps.core',
        'apps.geo',
        'apps.profile',
        'apps.registration',
        # 'apps.listings',
        # 'apps.organisations',
    )

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + SOCIAL_LOGIN_APPS


class Middleware(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.gzip.GZipMiddleware',
    )


class Static(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-files
    STATIC_ROOT = join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (join(BASE_DIR, 'assets'),)
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )


class Template(object):
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # local configuration app.
        'configuration.context_processors.site',
        # constance
        'constance.context_processors.config',
        # allauth specific context processors
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
    )
    TEMPLATE_DIRS = (join(BASE_DIR, 'templates'),)
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )


class Common(Authentication, Caching, Database, Email, Fixture, Localisation, Logging, Media, Models, Middleware,
             Static, Template):
    ROOT_URLCONF = 'configuration.urls'
    SITE_ID = 1
    WSGI_APPLICATION = 'configuration.wsgi.application'

    # App: apps.accounts settings
    USER_AVATAR = Static.STATIC_URL + "images/users/blank.png"
    # End

    # App: apps.geo settings
    MAPS_CENTER = (-41.3, 32)
    # End

    # ### Package: django-celery settings
    # See: http://rapidsms.readthedocs.org/en/0.16.0/topics/celery.html
    # BROKER_URL = "redis://vagrant:vagrant@localhost:6379/0"
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    # CELERY_IGNORE_RESULT = True
    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
    CELERY_TIMEZONE = "Europe/London"
    CELERY_ENABLE_UTC = True

    # store AsyncResult in redis
    CELERY_RESULT_BACKEND = "redis"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = "0"
    REDIS_VHOST = "0"  # have to check
    REDIS_USER = "vagrant"
    REDIS_PASSWORD = "vagrant"
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
    # CELERY_TASK_RESULT_EXPIRES =  3600
    CELERY_TASK_RESULT_EXPIRES = None
    REDIS_CONNECT_RETRY = True
    CELERY_SEND_EVENTS = True
    # CELERY_ACKS_LATE = True
    # REDIS_CONNECT_RETRY = True
    # CELERY_DISABLE_RATE_LIMITS = True
    # ### End Package: django-celery settings


    # Package: django-autoslug
    # AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'
    # end

    # Package: django-constance.
    # see: https://github.com/comoga/django-constance
    CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'  # using Redis (default)
    CONSTANCE_REDIS_CONNECTION = 'redis://localhost:6379/0'
    CONSTANCE_CONFIG = {
        'BLOG_PAGE_SIZE': (3, 'How many posts to show per page?'),
        'CONTACT_COMPANY_NAME': ('JobPlus Ltd', 'Name of Company'),
        'CONTACT_COMPANY_URL': ('http://www.jobplus.mu', 'URL of Company'),
        'CONTACT_ADDRESS_LINE1': ('589 Mongo Ave', 'Company Address Line 1'),
        'CONTACT_ADDRESS_LINE2': ('Port Louis', 'Company Address Line 2'),
        'CONTACT_ADDRESS_LINE3': ('Mauritius', 'Company Address Line 3'),
        'CONTACT_EMAIL_ENQUIRY': ('enquiries@jobplus.mu', 'Email for General Enquiries'),
        'CONTACT_PHONE_ENQUIRY': ('(+230) 717-8989 ', 'Phone number for enquiries'),
        'CURRENCY_SIGN': ('Rs.', 'Currency Abbreviation'),
        'FOOTER_COPYRIGHT': ('All Rights Reserved.', 'Copyright Message' ),
        'HOME_INTRO_CONTENT': ('Making Jobs a Dream!', 'Content message on home page.'),
        'HOME_INTRO_HEADING': ('Job Recruitment Made Easy', 'Intro Heading on home page.'),
        'SOCIAL_FACEBOOK_URL': ('http://www.facebook.com/jobplus', 'Facebook Link'),
        'SOCIAL_LINKEDIN_URL': ('http://www.linkedin.com/company/jobplus', 'LinkedIn Link'),
        'SOCIAL_TWITTER_URL': ('http://www.twitter.com/jobplus', 'Twitter Link'),
        'SOCIAL_PINTEREST_URL': ('http://www.pinterest.com/jobplus/', 'Pinterest Link'),
        'SOCIAL_GOOGLE_URL': ('http://plus.google.com/+jobplus', 'Google+ Link'),
        'SOCIAL_YOUTUBE_URL': ('https://www.youtube.com/user/jobplus', 'YouTube Link'),
        'SOCIAL_RSS_URL': ('http://www.jobplus.mu/feed/', 'Feed Link'),
        'SOCIAL_TWITTER_NAME': ('jobplus', 'Twitter username'),
        'SOCIAL_TWEET_COUNT': ('2', 'The number of recent tweets to show under the homepage.'),
        'SOCIAL_TWITTER_OAUTH_TOKEN': ('376877849-nIZrlmNAydPBO8eChPj6XS8AAAR2DIOQEOje8HUt', 'Twitter Access token'),
        'SOCIAL_TWITTER_OAUTH_SECRET': ('9PfoZpiufrSlovL63QAQuFmOEMhS2adcQKZoESrKuQfpb', 'Twitter Access token secret'),
        'SOCIAL_TWITTER_CONSUMER_KEY': ('Er6VXnvOqIctmKWJM1B1Yqm3o', 'Twitter Consumer key'),
        'SOCIAL_TWITTER_CONSUMER_SECRET': (
            'm9lJSShPHyRSWksP2LohnXLwupSv8vZ3NW89hWCBnmygehPnPV', 'Twitter Consumer secret'),
        'SYSTEM_EXCERPT_LENGTH': (300, 'Excerpt Length of Generated Summaries.'),
        'SYSTEM_IMAGES_PATH': ('/images/', 'Path to saving images'),
    }


    # Package: django-haystack
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
            'TIMEOUT': 60 * 5,
        },
    }
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
    # End


class Local(Common, Configuration):
    """
    The in-development settings and default configuration.
    """
    ALLOWED_HOSTS = []
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)
    SECRET_KEY = '9873KETNOEXA2121A'


    # start email settings
    # EMAIL_HOST = 'localhost'
    # EMAIL_PORT = 1025
    # EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    # end

    # installed apps.
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('debug_toolbar',)
    # end

    # start django-debug-toolbar settings.
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + \
                         (
                             'debug_toolbar.middleware.DebugToolbarMiddleware',
                         )
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        # ommited cause of the slow performance resolution of bower.js
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    )
    INTERNAL_IPS = ('127.0.0.1',
                    '10.0.2.2',  # Useful if using vagrant ## request.META['REMOTE_ADDR']
    )
    # end


class Staging(Common, Configuration):
    pass
    # DEBUG = False
    # TEMPLATE_DEBUG = DEBUG
    # SECRET_KEY = values.SecretValue()


class Production(Common, Configuration):
    """
    The production settings and default configuration.
    """
    ALLOWED_HOSTS = ['*']
    DEBUG = values.BooleanValue(False)
    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)
    SECRET_KEY = 'Youknowit!'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': values.BooleanValue(False),
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },

        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': values.BooleanValue(True),
            },
        }
    }
