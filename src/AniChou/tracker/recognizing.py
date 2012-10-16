# -*- coding: utf-8 -*-

import re
import os
import difflib
from AniChou import settings
from AniChou.db.models import Anime
from kaa import metadata

__doc__ = """
Regogniziging engine

The main function ("recognize") returns an Anime instance or None.

Filename processing:
----------------------
These functions filter the provided filename.

    clean_name: removes hashtags, subgroup and codecs
        Returns: the filterd anime name
    extract_name: removes all but the anime name.
        Returns: anime name
    extract_episode: removes all but the current watched episode
        Returns: current watched episode

------------------------------------------------------------

Regogniziging engine:
---------------------
This function provides functions to recognize the
current watched series and change the episode in the
local database.

    recognize: Evaluates a ratio of probable equally of the passed name
               and the entries in the local database, and choose best
               match.
        Returns: an Anime instance or false if matching level too low
"""

def recognize(filename):
    """
    Evaluates a ratio of probable equally of the passed name and the
    entries in the local database, and choose best match.
    Returns: an Anime instance or false if matching level too low
    """

    name = extract_name(filename)

    matching = []

    matcher = difflib.SequenceMatcher()
    matcher.set_seq2(name)

    # The essence machting algorithm
    for anime in Anime.objects.all():
        ratios = []
        for anime_name in anime.names:
            matcher.set_seq1(anime_name)
            ratios.append(matcher.ratio())
        matching.append((max(ratios), anime))

    # Sorting matching.
    matching.sort()

    if matching:
        (ratio, anime) = matching[-1]
        if ratio > settings.MATCHING_LEVEL:
            return anime
    return None


def clean_name(filename):
    """Get rid of hashtags, subgroup, codec and such"""
    # Should match all between [ , ], (, ) and gets rid of the file extension.
    # Monser RegEx ftw! :D
    reg = re.compile( \
        "((\[[\w\s&\$_.,+\!-]*\]*)|(\([\w\s&\$_.,+\!-]*\)*)|(.mkv)|(.mp4)|(.avi))")
    anime_raw = reg.sub("", filename)
    # replace underscores
    anime_raw = anime_raw.replace("_"," ")
    return anime_raw.strip()


def extract_name(filename):
    """Getting and returning anime name"""

    # Remove path from filename
    meta = metadata.parse(filename)
    #TODO: full usage of metadata.
    if meta.title:
        name = meta.title
    else:
        name = os.path.basename(filename)

    # Remove excess info
    name = clean_name(name)
    # Remove episode number
    name = re.sub("(ep\.?)?\s?\d+", "", name, re.I)
    # Remove all digits
    name = re.sub("[\d\._]{1,}", "", name)
    # Get rid of scores
    name = name.replace("-","")
    return name.strip()


def extract_episode(filename):
    """Getting and returning anime episode."""

    name = os.path.basename(filename)

    # Remove all but Numbers, witch must be at least a pair of two
    episode = re.sub("[a-zA-Z-+._&\s\!]{1,}", "", clean_name(name))

    return episode.strip()
