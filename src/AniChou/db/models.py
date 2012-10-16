# -*- coding: utf-8 -*-

from AniChou.db.base import Model
from AniChou.db.fields import ( NumberField, StringField,
        DatetimeField, ListField, DictField )
from datetime import date, datetime


LOCAL_ANIME_SCHEMA = {
    'title': unicode,
    'synonyms': set,
    'type': int,
    'episodes': int,
    'sources': dict,
    'air': int,
    'started': datetime,
    'ended': datetime,
    'my_episodes': int,
    'my_start': datetime,
    'my_finish': datetime,
    'my_score': int,
    'my_status': int,
    'my_updated': datetime
}


class Anime(Model):
    _scheme = LOCAL_ANIME_SCHEMA
    _unique = ('title', 'type', 'started')

    def get_names(self):
        return [self.title] + (self.synonyms or [])
    names = property(get_names)

    def save(self):
        self.my_updated = datetime.now()
        super(Anime, self).save()
