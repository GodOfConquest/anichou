# -*- coding: utf-8 -*-

import logging
import time
import urllib, urllib2
from cookielib import LWPCookieJar
from datetime import datetime, timedelta

from AniChou import settings
from AniChou.config import BaseConfig
from AniChou.db.models import Anime
from AniChou.db.manager import DoesNotExists
from AniChou.utils import ACRequest



class DefaultService(object):
    """
    Anime data base class. Reads and writes local anime data to disk, fetches and
    syncs with service server.

    Properties:
        name - human-readable name of service
        internalname - name of service for internal usage
        last_sync - date fo the last service sync
    """

    name = "Dummy service"
    decode_schema = {}

    def __init__(self, config=None, **kw):
        """
        Setup credentials, read local data and setup network connection
        environment. Optionally sync with service on startup.

        Does not take positional arguments. Keyword arguments can either be
        given individually (username, password, initsync) or as an
        ac_config() instance. This will not be retained.

        In the latter form we support some additional command line options.
        """

        self.internalname = self.__class__.__name__.lower()

        # When the architecture stabilizes, switch to config as the sole
        # positional argument, and retain it instead of copying parts.
        # That would also enable reconfiguration at runtime.
        self.setConfig(config or BaseConfig(), **kw)

        # setup cookie handler
        self.opener = urllib2.build_opener(
                        urllib2.HTTPCookieProcessor(LWPCookieJar()))
        self.opener.addheaders = [('User-Agent', u'Anichou/{0} {1}'.format(
                        self.__class__.__name__, settings.VERSION))]
        self._logined = None

        if self.initsync:
            self.sync()

    def _setLastSync(self, date):
        Anime.objects.db.setdefault('sync', {}
            ).setdefault('services', {}
            )[self.internalname] = date
    def _getLastSync(self):
        try:
            sync = Anime.objects.db['sync']['services'][self.internalname]
        except KeyError:
            self.last_sync = sync = datetime.now()
        return sync
    last_sync = property(_getLastSync, _setLastSync)

    anonymous = lambda self: not bool(self.username and self.password)

    def setConfig(self, cfg, **kwargs):
        """Setup self variables from config"""
        self.base_config  = cfg
        config = getattr(self.base_config.services, self.internalname)
        self.username = kwargs.get('username', config.get('username'))
        self.password = kwargs.get('password', config.get('password'))
        self.initsync = kwargs.get('initsync', self.base_config.startup.get('sync'))

    def stop(self):
        """
        Actions before service will be stopped.
        """
        logging.info("Service %s was disabled", self.name)

    def fetchURL(self):
        raise NotImplementedError('This function must be implemented in subclass')

    def pushURL(self, a):
        raise NotImplementedError('This function must be implemented in subclass')

    def cardURL(self):
        """Returns url for service item."""
        raise NotImplementedError('This function must be implemented in subclass')

    def guessRequest(self, anime):
        """Guess url and request method from anime.
        Useful for shit-like APIs with different methods for same actions.
        Returns: request_type_string, url_string, schema
        """
        raise NotImplementedError('This function must be implemented in subclass')

    def sync(self, filename=None):
        """
        Syncronize local anime database with the service server.
        (fetch -> compare -> push -> update local)
        Return:
            True on success, False for bad list
        """
        if filename:
            remote_list = open(filename).read()
        else:
            remote_list = self.fetchList()

        if not remote_list:
            return False

        # parse remote list and filter it
        remote_list = self.parseList(remote_list)
        (remote_updates, local_updates) = self.convertList(remote_list)
        self.logChanges(remote_updates, local_updates)

        # Try to update remote list
        if not self.pushList(local_updates):
            logging.warn('Your local data goes ouf of sync')
        Anime.objects.save()
        self.last_sync = datetime.now()
        return True

    def sendRequest(self, link, data={}, method=None):
        """
        Send request to the server. Return responce.
        """
        try:
            args = [link]
            if data:
                args.append(data)
            request = ACRequest(*args, method=method)
            response = self.opener.open(request)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                logging.error('Failed to reach %s server. Reason: %s',
                    self.name, e.reason)
            elif hasattr(e, 'code'):
                logging.error('The server couldn\'t fulfill the request. Error code %d',
                    e.code)
            return False
        return response

    def logined(self):
        if self._logined is None:
            self._logined = self.login()
        return self._logined

    def login(self):
        """
        Log in to service server.
        Returns: True on success, False on failure
        """
        raise NotImplementedError('Must be implemented in subclass')

    def fetchList(self):
        """
        Retrieve anime list from service server.
        Returns: remote data in its format.
        """
        # Three way switch: login (un)successfull or don't even try.
        if self.anonymous() or not self.logined():
            logging.warn('Login to %s server failed..', self.name)
            return None
        fetch_response = self.sendRequest(self.fetchURL())
        if fetch_response:
            return fetch_response.read()
        return []

    def pushList(self, local_updates):
        """
        Updates every entry in the local updates dictionary on the server.
        Returns:
            True on success, False on failure
        """
        if self.anonymous() or not self.logined():
            logging.warn('Login to %s server failed..', self.name)
            return None

        for anime in local_updates:
            request_type, url, schema = self.guessRequest(anime)
            postdata = urllib.urlencode(self.encode(anime, schema))
            response = self.sendRequest(url, postdata, method=request_type)
            if not response:
                return False
            time.sleep(settings.TIMEOUT)
        return True

    def parseList(self, remote_list):
        """
        Parse remote list and return it in internal format.
        """
        raise NotImplementedError('Must be implemented in subclass')

    def convertList(self, recieved_list):
        """
        Convert recieved service list to local format.
        Returns:
           remote_updates: changes that are more up to date on the server
           local_updates: changes that are more up to date locally
        """
        remote_updates = []
        local_updates = []
        td = timedelta(0)
        updated = self.last_sync
        for item in recieved_list:
            decoded = self.decode(item)
            try:
                # FIXME: rewrite this
                started = decoded.get('started', None)
                if not started or \
                        started - type(started)(1,1,1) == td:
                    started = '*'
                anime = Anime.objects.get(names__in=decoded['title'],
                                type=decoded['type'],
                                started=started)
            except DoesNotExists:
                anime = Anime(**decoded)
                anime.save()
                remote_updates.append(anime)
                continue
            updated = decoded.get('my_updated', updated)
            if anime._changed < updated:
                remote_updates.append(anime)
                anime.update(decoded)
                anime.save()
            elif anime._changed > updated:
                local_updates.append(anime)
            else:
                logging.warning(
                    'Updating behawior of item {0} was not defined.'.format(Anime.title))
        return remote_updates, local_updates

    def decode(self, item, schema=None):
        """
        Convert item dictionary form remote service schema to local
        schema `db.models.LOCAL_ANIME_SCHEMA`. Service must provide
        convert list as schema parameter.
        Returns: converted dictionary
        """
        schema = getattr(self, 'decode_schema', schema)
        if not schema:
            raise NotImplementedError('Must be called with convert list')
        ret = {}
        for key, value in schema:
            if not key in item.keys():
                continue # Schema key not found, schema error maybe?
            ret[value] = self.decodeField(value, item[key])
        return ret

    def decodeField(self, name, value):
        """
        Make convert proceduer for specific fields
        """
        raise NotImplementedError('Must be implemented in subclass')

    def encode(self, item, schema=None):
        """
        Convert Anime item to item dictionary using remote service
        schema. Service must provide convert list as schema parameter.
        Returns: converted dictionary
        """
        schema = getattr(self, 'encode_schema', schema)
        if not schema:
            raise NotImplementedError('Must be called with convert list')
        ret = {}
        for key, value in schema:
            if not hasattr(item, key):
                logging.error('Schema key %s not found in Anime model', key)
                continue
            ret[value] = self.encodeField(key, getattr(item, key))
        return ret

    def encodeField(self, name, value):
        """
        Make convert proceduer for specific fields
        """
        raise NotImplementedError('Must be implemented in subclass')

    def logChanges(self, remote, local):
        """
        Writes changes to logfile.
        """
        for action, array in (('Fetched', remote), ('Pushing', local)):
            for anime in array:
                logging.info(u'{0} {1} with {2} episodes.'.format(action,
                         anime.title, unicode(anime.my_episodes)))
