
import threading
import time
from AniChou import settings
from AniChou import signals
from AniChou.db.models import LOCAL_STATUS_R
from AniChou.tracker import players
from AniChou.tracker.recognizinig import recognize, extract_episode

__doc__ = """Watcher thread
This module provides watcher class for the tracker.
Watcher is thread which check currently played files for match with
database entities and change status of found entity.
"""

class Watcher(threading.Thread):

    _exit = False

    def __init__(self, cfg):
        self.cfg = cfg
        self.trackmessage = signals.Signal()
        self.trackmessage.connect('set_track_message')

    def run(self):
        while not self._exit:
            track = players.get_playing(settings.PLAYERS, self.cfg.search_dirs)
            for key, value in track:
                anime = recognize(key)
                # FIXME: does watcher must update anime by itself?
                # Maybe change to some signal
                if not anime:
                    continue
                try:
                    episode = int(extract_episode(key))
                except (ValueError, TypeError):
                    episode = 1
                signals.emit(self.trackmessage, None,
                    u'Playing: {0} -- Episode: {1}'.format(m, episode))
                if anime.my_status != LOCAL_STATUS_R['completed']:
                    anime.my_status = LOCAL_STATUS_R['watching']
                if anime.my_episodes < episode - 1:
                    anime.my_episodes = episode
                    anime.my_updated = datetime.datetime.now()
                anime.save()
            time.sleep(settings.TRACKING_INTERVAL)

