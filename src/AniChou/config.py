
import os, getopt, sys
import json

# AniChou
import settings


def usage(prog):
    """
    Print command line help.

    Takes an application name to display.
    """
    # Won't strip indentation.
    logging.info("""
    Usage: %s [options]

    Options:
      --version       show program's version number and exit
      -h, --help      show this help message and exit
      -d, --no-gui    disable GUI
      -t, --tracker   enable play-tracker
      -c <file>       use an alternative configuration file
      -r              overwrite config with default values
      -f <file>       load data from file (Not supported)

    Developers only:
      -a              disable login and site updates

    """, prog)


def options(prog, version, argv):
    """
    Return options found in argv.
    prog will be to usage() when --help is requested.
    version will be printed for --version.
    The first items of argv must be an option, not the executable name like
    in sys.argv!
    The result has the format {section: {option: value}}
    """
    # For getopt we have to mention each option several times in the code,
    # unlike with the optparse module. But then that's more readable.
    # Also optparse doesn't keep information on which options where
    # actually given on the command line versus the hard-coded defaults.
    try:
        opts, args = getopt.getopt(argv, "hdtc:arf:", ["version", "help",
            "no-gui", "tracker", "config=", "anonymous", "reset"])
    except getopt.GetoptError, err:
        logging.error(err)
        usage(prog)
        sys.exit(2)
    given = {}
    for o, a in opts:
        if o == "--version":
            logging.info("%s %s", prog, version)
            sys.exit()
        elif o in ("-h", "--help"):
            usage(prog)
            sys.exit()
        elif o in ("-d", "--no-gui"):
            given.setdefault("startup", {})["gui"] = False
        elif o in ("-t", "--tracker"):
            given.setdefault("startup", {})["tracker"] = True
        elif o == "-c":
            given.setdefault(None, {})["config"] = a
        elif o == "-a":
            given.setdefault("login", False)
        elif o == "-r":
            given.setdefault(None, {})["reset"] = True
        else:
            assert False, "getopt knew more than if"
    return given


class Config(dict):

    def __init__(self, indict=None):
        if indict is None:
            indict = {}
        dict.__init__(self, indict)

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            c = Config()
            self.__setattr__(item, c)
            return c

    def __setattr__(self, item, value):
        if self.__dict__.has_key(item):
            dict.__setattr__(self, item, value)
        else:
            if isinstance(value, dict):
                self.__setitem__(item, Config(value))
            else:
                self.__setitem__(item, value)


default_opts = {
    'startup': {
        'gui': True,
        'sync': False,
        'tracker': False,
        'last_dir': os.path.expanduser('~'),
    },
    'services': Config({
        'default': settings.DEFAULT_SERVICE
    }),
    'search_dirs': [
        os.path.expanduser('~'),
    ],
}

run_opts = options(os.path.basename(sys.argv[0]), settings.VERSION, sys.argv[1:])


class BaseConfig(Config):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(
                                    cls, *args, **kwargs)
        return cls._instance

    def __init__(self, indict=None):
        if indict is None:
            indict = {}
        indict = dict(default_opts.items() + run_opts.items() + indict.items())
        dict.__init__(self, indict)
        self.load()

    def save(self):
        stream = file(settings.CONFIG_PATH, 'w')
        json.dump(dict(self), stream)

    def load(self):
        try:
            stream = file(settings.CONFIG_PATH, 'rU')
        except:
            pass
        else:
            d = json.load(stream)
            for key, value in d.items():
                setattr(self, key, value)
