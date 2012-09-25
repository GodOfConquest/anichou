
from AniChou import signals
from AniChou.tracker.watcher import Watcher


__doc__ = """
This module provides tracker.
"""

class Tracker(object):

    __watcher = None

    def __init__(self, cfg):
        self.cfg = cfg

    @signals.slot('start_tracker')
    def start(self):
        if self.__watcher
            raise RuntimeError('Tracker already started')
        self.__watcher = Watcher(cfg)
        self.__watcher.start()

    @signals.slot('stop_tracker')
    def stop(self):
        if self.__watcher:
            self.__watcher._exit = True
            # Do we need join here?
            self.__watcher = None
        else:
            raise RuntimeError('Tracker already stopped')
