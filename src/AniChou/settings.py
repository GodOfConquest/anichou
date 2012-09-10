
""" settings -- global constants

We try to keep global constans as few as possible, but things like path and
user directory sturcture might change, and to make this kind of transitions as
painless as possible we put them in one place. Here.
"""

from os import path


# Current version string
VERSION = '9.1.6-beta'

# Path to the user directory of anichou (where data, config and plugins
# are stored).
USER_PATH = path.join(path.expanduser('~'), '.anichou')

# Package base path (where the module script files are located)
PACKAGE_PATH = path.abspath(path.dirname(__file__))

# Path to the configuration file
CONFIG_PATH = path.join(USER_PATH, 'ac.cfg')

# Log settings
LOG_ERROR_FORMAT = "%(levelname)s at %(asctime)s in %(funcName)s in %(filename) at line %(lineno)d: %(message)s"
LOG_ERROR_DATE = '[%d.%m.%Y %I:%M:%S]'
LOG_DEBUG_FORMAT = "%(asctime)s: %(message)s"
LOG_PATH = path.join(USER_PATH, 'ac.log')
LOG_CONFIG_PATH = path.join(PACKAGE_PATH, 'data', 'logging.cfg')
LOG_CONFIG = {'version': 1,
              'formatters': {'error': {'format': LOG_ERROR_FORMAT,
                                       'datefmt': LOG_ERROR_DATE},
                             'debug': {'format': LOG_DEBUG_FORMAT,
                                       'datefmt': '[%d %b %I:%M:%S]'}},
              'handlers': {'console': {'class': 'logging.StreamHandler',
                                       'formatter': 'debug',
                                       'level': 'logging.DEBUG'},
                          'file': {'class':'logging.handlers.RotatingFileHandler',
                                   'args': (LOG_PATH,'a','maxBytes=10000','backupCount=5'),
                                   'formatter':'error',
                                   'level': 'logging.ERROR'}},
              'root': {'handlers': ('console', 'file'), 'level': 'DEBUG'}}


# Path to data file
DATA_PATH = path.join(USER_PATH, 'ac.dat')

DEFAULT_SERVICE = 'mal'

# Plugin path
PLUGIN_PATH = path.join(USER_PATH, 'plugins')

# Timeout for requests. Make ambigious number of requerst per second
# is bad. Spare the servers.
TIMEOUT = 0.001

# Interval between two tracking attempts
TRACKING_INTERVAL = 1000

# List of players processes names for tracking
PLAYERS = ['mplayer', 'totem']
