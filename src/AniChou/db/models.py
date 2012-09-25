
from AniChou.db.base import Model
from AniChou.db.fields import ( NumberField, StringField,
        DatetimeField, ListField, DictField )
from datetime import date, datetime


LOCAL_STATUS = [
    (0, u'None'),
    (1, u'Watching'),
    (2, u'Plan to watch'),
    (3, u'Completed'),
    (4, u'Dropped'),
    (5, u'Hold'),
    (6, u'Partially watched'),
]


LOCAL_STATUS_DICT = dict(LOCAL_STATUS)


LOCAL_STATUS_R = {
    u'none': 0,
    u'watching': 1,
    u'plantowatch': 2,
    u'completed': 3,
    u'dropped': 4,
    u'hold': 5,
    u'partially': 6
}


LOCAL_ANIME_SCHEMA = {
    'title': unicode,
    'synonyms': set,
    'type': int,
    'episodes': int,
    'sources': dict,
    'status': int,
    'started': datetime,
    'ended': datetime,
    'image': list,
    'my_episodes': int,
    'my_start': date,
    'my_finish': date,
    'my_score': int,
    'my_status': int,
    'my_updated': datetime
}


class Anime(Model):
    _scheme = LOCAL_ANIME_SCHEMA

    def names(self):
        return [self.titile] + self.synonyms
