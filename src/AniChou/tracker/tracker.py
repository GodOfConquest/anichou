
from AniChou import signals
from AniChou.tracker.watcher import Watcher


__doc__ = """
This module provides tracker.
"""


__all__ = ['start', 'stop', 'set_config']

WATCHER = False
CONFIG = None

def set_config(cfg):
    global CONFIG
    CONFIG = cfg


@signals.Slot('start_tracker')
def start():
    global WATCHER
    global CONFIG
    if WATCHER:
        raise RuntimeError('Tracker already started')
    WATCHER = Watcher(CONFIG)
    WATCHER.start()


@signals.Slot('stop_tracker')
def stop():
    global WATCHER
    if WATCHER:
        WATCHER._exit = True
        # Do we need join here?
        WATCHER = None
    else:
        raise RuntimeError('Tracker already stopped')
