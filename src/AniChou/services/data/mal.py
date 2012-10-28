# -*- coding: utf-8 -*-

# Copyright (c) 2008 Gareth Latty
# Copyright (c) 2009 Sebastian Bartos
# Copyright (c) 2009 Andre 'Necrotex' Peiffer
# Copyright (c) 2012 Sir Anthony
# See COPYING for details

""" mal.py -- core data schemas

This module contains the core data schemas used in the applicaiton and in the
communication with the server.
"""

from datetime import date, datetime

## ANIME schema of the xml data the MyAnimeList server sends
anime_schema = {
    'series_animedb_id': int,
    'series_title': unicode,
    'series_synonyms': unicode,
    'series_type': unicode,
    'series_episodes': int,
    'series_status': unicode,
    'series_start': date,
    'series_end': date,
    'series_image': unicode,
    'my_id': int,
    'my_watched_episodes': int,   # push argument
    'my_start_date': date,
    'my_finish_date': date,
    'my_score': int,   # push argument
    'my_status': unicode,   # push argument
    'my_rewatching': int,
    'my_rewatching_ep': int,
    'my_last_updated': datetime   # sync variable
}


anime_convert = (
    ('series_animedb_id', 'sources'),
    ('series_title', 'title'),
    ('series_synonyms', 'synonyms'),
    ('series_type', 'type'),
    ('series_episodes', 'episodes'),
    ('series_status', 'air'),
    ('series_start',  'started'),
    ('series_end', 'ended'),
    ('my_watched_episodes', 'my_episodes'),
    ('my_start_date', 'my_start'),
    ('my_finish_date', 'my_finish'),
    ('my_score', 'my_score'),
    ('my_status', 'my_status'),
    ('my_last_updated', 'my_updated')
)


anime_convert_json_default = (
    ('id', 'series_animedb_id'),
    ('title', 'series_title'),
    ('other_titles', 'series_synonyms'),
    ('type', 'series_type'),
    ('image_url', 'series_image'),
    ('episodes', 'series_episodes'),
    ('status', 'series_status'),
    ('start_date', 'series_start'),
    ('end_date', 'series_end'),
    ('listed_anime_id', 'my_id'),
    ('watched_episodes', 'my_watched_episodes'),
    ('score', 'my_score'),
    ('watched_status', 'my_status')
)


anime_del_schema = [] # No params
anime_post_schema = [
    ('sources', 'anime_id'),
    ('my_status', 'status'),
    ('my_episodes', 'episodes'),
    ('my_score', 'score')
]
anime_put_schema = [
    ('my_status', 'status'),
    ('my_episodes', 'episodes'),
    ('my_score', 'score')
]


### This is schema of data recieved using mal-api.com
anime_schema_json = {
    'id': int,
    'title': unicode,
    'other_titles': dict,
    'synopsis': unicode,
    'type': unicode,
    'rank': int,
    'popularity_rank': int,
    'image_url': unicode,
    'episodes': int,
    'status': unicode,
    'start_date': unicode,
    'end_date': unicode,
    'genres': list,
    'tags':list,
    'classification': unicode,
    'members_score': float,
    'members_count': int,
    'favorited_count': int,
    'manga_adaptations': list,
    'prequels': list,
    'sequels': list,
    'side_stories': list,
    'parent_story': list,
    'character_anime': list,
    'spin_offs': list,
    'summaries': list,
    'alternative_versions': list,
    'listed_anime_id': int,
    'watched_episodes': int,
    'score': 0,
    'watched_status': unicode
}


MAL_STATUS = {
    1: "watching", # 1
    2: "plantowatch", # 6 "plan to watch"/"plantowatch"
    3: "completed", # 2
    4: "dropped", # 4
    5: "onhold", # 3 "on-hold"/
    6: "watching", # u'Partially watched',
}
