
LOCAL_STATUS = [
    (0, u'None'),
    (1, u'Watching'),
    (2, u'Plan to watch'),
    (3, u'Completed'),
    (4, u'Dropped'),
    (5, u'Hold'),
    (6, u'Partially watched'),
]

LOCAL_STATUS_R = {
    u'none': 0,
    u'watching': 1,
    u'plantowatch': 2,
    u'completed': 3,
    u'dropped': 4,
    u'hold': 5, u'on-hold': 5,
    u'partially': 6
}

LOCAL_TYPE = [
    (0, u'TV'),
    (1, u'Movie'),
    (2, u'OVA'),
    (3, u'SMovie'),
    (4, u'Special'),
    (5, u'ONA'),
    (6, u'Music')
]

LOCAL_TYPE_R = {
    'tv': 0,
    'movie': 1,
    'ova': 2, 'oav': 2,
    'smovie': 3,
    'special': 4,
    'ona': 5,
    'music': 6,
}

LOCAL_AIR = [
    (0, 'Not aired'),
    (1, 'Currently airing'),
    (2, 'finished airing')
]

LOCAL_AIR_R = {
    'not aired': 0,
    'currently airing': 1,
    'finished airing': 2,
}
