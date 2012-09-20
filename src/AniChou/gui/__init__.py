
import logging
import signal
import sys

__all__ = ['Qt', 'notify']


# Global is bad, but we do not need gui manager class yet
APP = None


def Qt(manager, cfg):
    from AniChou.gui import qtctl
    from AniChou.utils import excepthook
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.excepthook = qtctl
    APP = qtctl.get_app(sys.argv)
    window = qtctl.Main(manager, cfg)
    # Write all exceptions to log
    sys.excepthook = excepthook
    window.show()
    e = APP.exec_()
    #sys.exit(e)


def notify(message):
    logging.info(message)
    if APP:
        APP.notify(message)


