
import logging
import signal
import sys

from AniChou.gui import qtctl

__all__ = ['Qt', 'notify']


# Global is bad, but we do not need gui manager class yet
APP = None


def Qt(manager, cfg):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    APP = qtctl.get_app(sys.argv)
    window = qtctl.Main(manager, cfg)
    window.show()
    e = APP.exec_()
    #sys.exit(e)


def notify(message):
    logging.info(message)
    if APP:
        APP.notify(message)


