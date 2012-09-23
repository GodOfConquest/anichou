
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
    'synonyms': list,
    'type': int,
    'episodes': int,
    'sources': dict,
    'series_status': int,
    'series_start': datetime,
    'series_end': datetime,
    'image': list,
    'status_episodes': int,
    'status_start': date,
    'status_finish': date,
    'status_score': int,
    'status_status': int,
    'status_updated': datetime
}


class Anime(Model):
    _scheme = LOCAL_ANIME_SCHEMA
