# -*- coding: utf-8 -*-

import cPickle
from os import path
from AniChou import settings

class PickleDB(dict):
    """
    Database module. Reads and writes to local database.

    """
    def __init__(self):
        dict.__init__(self, {})
        self.read()

    def write(self, data):
        """
        Takes a dictionary object to store into the DB
        """
        db_handle = open(settings.DATA_PATH, 'wb')
        cPickle.dump(dict(self), db_handle)
        db_handle.close()

    def read(self):
        """
        Reads from db.
        """
        if path.isfile(settings.DATA_PATH):
            db_handle = open(settings.DATA_PATH, 'rb')
            db_handle.seek(0)
            self.clear()
            try:
                self.update(cPickle.load(db_handle))
            except EOFError:
                pass
            db_handle.close()
