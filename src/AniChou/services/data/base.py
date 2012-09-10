
# Lol, copyright? Here?


""" base.py -- core data schemas

This module contains the core data schemas used in the local database.
"""

from datetime import date, datetime


LOCAL_ANIME_SCHEMA = {
    'id': int,
    'title': unicode,
    'synonyms': unicode,
    'type': int,
    'episodes': int,
    'sources': list,
    'series_status': int,
    'series_start': date,
    'series_end': date,
    'image': unicode,
    'status_id': int,
    'status_episodes': int,       # push argument
    'status_start': date,
    'status_finish': date,
    'status_score': int,          # push argument
    'status_status': int,         # push argument
    'status_rewatching': int,
    'status_rewatching_ep': int,
    'status_updated': datetime    # sync variable
}


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
