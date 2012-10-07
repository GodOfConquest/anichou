
# Copyright (c) 2008 Gareth Latty
# Copyright (c) 2009 Sebastian Bartos
# Copyright (c) 2009 Andre 'Necrotex' Peiffer
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


## This is old, probably obsolete data inhirited from original AniChou.
## It has no usage now.


## Here is a sample of the data representation the myanimelist module produces,
## and which is used in the application and is also sent to the persistent data
## file. This example data has 2 entries, one with a unicode character in it to
## demonstarte key encoding. Note: some date keys may be missing in enries, for
## instance the start and end keys if they are 0000-00-00 on the server.
## Note2: if additional keys are added in the XML, they will appear as unicode
## strings in the datastructures.
##
## You can access this data with an anime_data instance db property:
##    adata.db['Macross Frontier']   # gives a dict with all the properites of
##                                     the Macross Frontier anime entry
##    adata.db['Macross Frontier']['my_status']   # gives the current status of
##                                                  the above (2 in this case)
##
## { 'Lucky \xe2\x98\x86 Star': {u'my_id': 12345,
##                             u'my_last_updated':
##                                   datetime.datetime(2009, 3, 26...),
##                             u'my_rewatching': 0,
##                             u'my_rewatching_ep': 0,
##                             u'my_score': 0,
##                             u'my_start_date': datetime.date(2009, 3, 25),
##                             u'my_status': 1,
##                             u'my_watched_episodes': 8,
##                             u'series_animedb_id': 1887,
##                             u'series_end': datetime.date(2007, 9, 17),
##                             u'series_episodes': 24,
##                             u'series_image':
##                        u'http://cdn.myanimelist.net/images/anime/2/4781.jpg',
##                             u'series_start': datetime.date(2007, 4, 9),
##                             u'series_status': 2,
##                             u'series_synonyms':
##                                 u'Lucky Star; Raki \u2606 Suta',
##                             u'series_title': u'Lucky \u2606 Star',
##                             u'series_type': 1},
## 'Macross Frontier': {u'my_id': 12345,
##                      u'my_last_updated': datetime.datetime(2008, 11, 22...),
##                      u'my_rewatching': 0,
##                      u'my_rewatching_ep': 0,
##                      u'my_score': 9,
##                      u'my_status': 2,
##                      u'my_watched_episodes': 25,
##                      u'series_animedb_id': 3572,
##                      u'series_end': datetime.date(2008, 9, 25),
##                      u'series_episodes': 25,
##                      u'series_image':
##                  u'http://cdn.myanimelist.net/images/anime/10/10549.jpg',
##                      u'series_start': datetime.date(2008, 4, 3),
##                      u'series_status': 2,
##                      u'series_synonyms': u'Macross F',
##                      u'series_title': u'Macross Frontier',
##                      u'series_type': 1}}

## MANGA schema of the xml data the MyAnimeList server sends
mal_manga_data_schema = {
    'series_mangadb_id': int,
    'series_title': unicode,
    'series_synonyms': unicode,
    'series_type': int,
    'series_chapters': int,
    'series_volumes': int,
    'series_status': int,
    'series_start': date,
    'series_end': date,
    'series_image': unicode,
    'my_id': int,
    'my_read_chapters': int,   # push argument
    'my_read_volumes': int,   # push argument
    'my_start_date': date,
    'my_finish_date': date,
    'my_score': int,   # push argument
    'my_status': int,   # push argument
    'my_rereadingg': int,
    'my_rereading_chap': int,
    'my_last_updated': datetime}   # sync variable


## Anime Datastructure for the MAL API
mal_api_anime_schema = {
    'episode' :  int,
    'status': int, #OR string. 1/watching, 2/completed, 3/onhold, 4/dropped, 6/plantowatch
    'score' : int,
    'downloaded_episodes' : int,
    'storage_type' : int, # (will be updated to accomodate strings soon)
    'storage_value': float,
    'times_rewatched' : int,
    'rewatch_value' : int,
    'date_start' : date, #mmddyyyy
    'date_finish' : date, #mmddyyyy
    'priority' : int,
    'enable_discussion' : int, #1=enable, 0=disable
    'enable_rewatching' : int, #1=enable, 0=disable
    'comments' : str,
    'fansub_group' : str,
    'tags. string' : list #tags separated by commas
}

## Manga Datastructure for the MAL API
mal_api_manga_schema = {
    'chapter' : int,
    'volume' : int,
    'status' : int, #OR string. 1/reading, 2/completed, 3/onhold, 4/dropped, 6/plantoread
    'score' : int,
    'downloaded_chapters' : int,
    'times_reread' : int,
    'reread_value' : int,
    'date_start' : date, #mmddyyyy
    'date_finish' : date, #mmddyyyy
    'priority' : int,
    'enable_discussion' : int, #1=enable, 0=disable
    'enable_rereading' : int, #1=enable, 0=disable
    'comments' : str,
    'scan_group' : str,
    'tags. string' : list,
    'retail_volumes' : int}
