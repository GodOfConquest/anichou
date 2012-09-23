# =========================================================================== #
# Name:     database.py
# Purpose:  Read and write to the local database
#
# Copyright (c) 2009 Daniel Anderson - dankles/evilsage4
#
# License: GPL v3, see COPYING file for details
# =========================================================================== #

import cPickle
from os import path
from AniChou import settings

class PickleDB(dict):
    """
    Database module. Reads and writes to local database.

    """
    def __init__(self):
        dict.__init__(self, {})

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
        if not self.local_db:
            if path.isfile(settings.DATA_PATH):
                db_handle = open(settings.DATA_PATH, 'rb')
                self.clear()
                self.update(cPickle.load(db_handle))
                db_handle.close()
        return self.local_db
