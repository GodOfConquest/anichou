# -*- coding: utf-8 -*-

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
LOG_ERROR_FORMAT = u"%(levelname)s at %(asctime)s in %(funcName)s in %(filename)s at line %(lineno)d: %(message)s"
LOG_ERROR_DATE = u'[%d.%m.%Y %I:%M:%S]'
LOG_DEBUG_FORMAT = u'%(asctime)s: %(message)s'
#LOG_ERROR_FORMAT = LOG_DEBUG_FORMAT
LOG_PATH = path.join(USER_PATH, 'ac.log')
LOG_CONFIG_PATH = path.join(PACKAGE_PATH, 'data', 'logging.cfg')
LOG_CONFIG = {'version': 1,
              'formatters': {'error': {'()': 'AniChou.uformatter.UnicodeFormatter',
                                       'format': LOG_ERROR_FORMAT,
                                       'datefmt': LOG_ERROR_DATE},
                             'debug': {'()': 'AniChou.uformatter.UnicodeFormatter',
                                       'format': LOG_DEBUG_FORMAT,
                                       'datefmt': u'[%d %b %I:%M:%S]'}},
              'handlers': {'console': {'class': 'logging.StreamHandler',
                                       'formatter': 'debug',
                                       'level': 'DEBUG'},
                          'file': {'class':'logging.handlers.RotatingFileHandler',
                                   'filename': LOG_PATH, 'maxBytes': 100000,
                                   'backupCount': 5, 'formatter':'error',
                                   'level': 'ERROR'}},
              'root': {'handlers': ('console', 'file'), 'level': 'DEBUG'}}


# Path to data file
DATA_PATH = path.join(USER_PATH, 'ac.dat')

DEFAULT_SERVICE = 'mal'
SERVICES = ['mal']

# Plugin path
PLUGIN_PATH = path.join(USER_PATH, 'plugins')

# Timeout for requests. Make ambigious number of requerst per second
# is bad. Spare the servers.
TIMEOUT = 0.001

# Interval between two tracking attempts
TRACKING_INTERVAL = 300

# Recognizing minimum matching level
MATCHING_LEVEL = 0.3

# List of players processes names for tracking
PLAYERS = ['mplayer', 'totem']


# GUI Settings

GUI_COLUMNS = {
    'name': (
        (0, 'changed'),
        (1, 'title'),
        (2, 'type'),
        (3, 'sources'),
        (4, 'my_score'),
        (5, 'episodes'),
        (6, 'progress')
    ),
    'title': (
        (0, ''),
        (1, 'Title'),
        (2, 'Type'),
        (3, 'Sources'),
        (4, 'Rating'),
        (5, 'Episodes'),
        (6, 'Progress')
    ),
    'size': (
        (0, 7), (1, 300), (2, 50), (3, 60), (4, 50), (5, 70)
    ),
    'controls': (
        (0, 'Color'), (4, 'ComboBox'), (5, 'SpinBox'), (6, 'ProgressBar')
    )

}
