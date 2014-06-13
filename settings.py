import logging
import tornado
import tornado.template
import os
import redis
from tornado.options import define, options

import logconfig

# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
tornado.options.parse_command_line()


############################
# Deployment Configuration #
############################


class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

DEBUG = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug

############
# METADATA #
############

OPERATION_COUNTRY = 'Singapore'
SITE_OWNER = 'Brandsfever Pte. Ltd.'

FACEBOOK_USERNAME = TWITTER_USERNAME = 'brandsfever'
GOOGLE_PLUS_PAGE_ID = '102601714294044778221'
BLOG_URL = 'http://www.brandsfever.com/blog/'

STATIC_URL = '/static'
if DEBUG:
    API_BASE_URI = 'http://127.0.0.1:8000/api/v5'
    GO_API_BASE_URI = 'http://127.0.0.1:9090'
    SITE_HTTP_URL = 'http://127.0.0.1:8888'
    SITE_HTTPS_URL = 'https://127.0.0.1:8888'
    BRANDSFEVER_SG_HTTP_URL = 'http://127.0.0.1:8000'
    BRANDSFEVER_SG_HTTPS_URL = 'http://127.0.0.1:8000'
else:
    API_BASE_URI = 'https://www.brandsfever/api/v5'
    GO_API_BASE_URI = 'https://api-1.brandsfever.com'
    SITE_HTTP_URL = ''
    SITE_HTTPS_URL = ''
    BRANDSFEVER_SG_HTTP_URL = '//www.brandsfever.com'
    BRANDSFEVER_SG_HTTPS_URL = 'https://www.brandsfever.com'

if DEBUG:
    SESSION_COOKIE_DOMAIN = "127.0.0.1"
else:
    SESSION_COOKIE_DOMAIN = ""
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
COOKIE_SECRET = "your-cookie-secret"
LOGIN_URL = "/login/"

#################
# SITE CURRENCY #
#################

SITE_CURRENCY = "SGD"

##########################
# LOCAL SETTINGS RELATED #
##########################

try:
    from local_settings import *
except ImportError:
    INSTANCE_TYPE = "luxury"

MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')

settings = {}
settings['debug'] = DEBUG
settings['static_path'] = MEDIA_ROOT
settings['xsrf_cookies'] = True
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)

SYSLOG_TAG = "transformers"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
    'loggers': {
        'transformers': {},
    },
}

if settings['debug']:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

logconfig.initialize_logging(
    SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS,
    LOG_LEVEL, USE_SYSLOG)

if options.config:
    tornado.options.parse_config_file(options.config)


settings['cookie_secret'] = COOKIE_SECRET
settings['login_url'] = LOGIN_URL

################
# Redis Config #
################

REDIS_POOL = redis.ConnectionPool(host='192.168.1.66', port=6379, db=10)

try:
    from extra_settings import *
except ImportError:
    pass
