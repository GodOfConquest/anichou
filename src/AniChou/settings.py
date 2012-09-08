
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

# Path to the configuration file
CONFIG_PATH = path.join(USER_PATH, 'ac.cfg')

# Path to log file
LOG_PATH = path.join(USER_PATH, 'ac.log')

# Path to data file
DATA_PATH = path.join(USER_PATH, 'ac.dat')

DEFAULT_SERVICE = 'mal'

# Plugin path
PLUGIN_PATH = path.join(USER_PATH, 'plugins')

# Package base path (where the module script files are located)
PACKAGE_PATH = path.abspath(path.dirname(__file__))

# Timeout for requests. Make ambigious number of requerst per second
# is bad. Spare the servers.
TIMEOUT = 0.001
