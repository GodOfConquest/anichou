# -*- coding: utf-8 -*-

import logging
import signal
import sys


__all__ = ['Qt']


def Qt(manager, cfg):
    from AniChou.gui import qtctl
    from AniChou.utils import excepthook
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = qtctl.get_app(sys.argv)
    window = qtctl.Main(manager, cfg)
    # Write all exceptions to log
    sys.excepthook = excepthook
    window.show()
    e = app.exec_()
    #sys.exit(e)





