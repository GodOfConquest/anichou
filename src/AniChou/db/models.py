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
    _schema = LOCAL_ANIME_SCHEMA
    _unique = ('title', 'type', 'started')
    _updated_fields = ('sources', 'synonyms', 'title')


    def get_names(self):
        return [self.title] + (self.synonyms or [])
    names = property(get_names)

    def save(self):
        self.my_updated = datetime.now()
        super(Anime, self).save()

    def sources_update(self, value):
        if not self.sources:
            self.sources = {}
        self.sources.update(value)
        print value
        print self.sources

    def title_update(self, value):
        if value == self.title:
            return
        if self.title:
            self.synonyms_update(value)
        else:
            setattr(self, 'title', value)

    def synonyms_update(self, value):
        if not self.synonyms:
            self.synonyms = set()
        if type(value) is set:
            self.synonyms |= value
        else:
            self.synonyms.add(value)
