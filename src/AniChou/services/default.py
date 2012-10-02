
import logging
import urllib2
from cookielib import LWPCookieJar
from datetime import datetime

from AniChou.config import BaseConfig
from AniChou.db.models import Anime
from AniChou.db.manager import DoesNotExists
from AniChou import settings



class DefaultService(object):
    """
    Anime data base class. Reads and writes local anime data to disk, fetches and
    syncs with service server.

    username: login username
    password: login password
    db_path: path to database
    db: local anime database that is a nested dict and has ASCII-fied series
        titles as keys and and fields form mal_anime_data_schema as dict data.
    """

    name = "Dummy service"
    decode_schema = {}
    decodable_fields = {}

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

        self.encode_schema = dict([(value, key) for key, value in self.decode_schema])

        # setup cookie handler
        self.opener = urllib2.build_opener(
                        urllib2.HTTPCookieProcessor(LWPCookieJar()))
        self.opener.addheaders = [('User-Agent', u'Anichou/{0} {1}'.format(
                        self.__class__.__name__, settings.VERSION))]

        if self.initsync:
            self.sync()

    def setConfig(self, cfg, **kwargs):
        """Setup self variables from config"""
        self.base_config  = cfg
        config = getattr(self.base_config.services, self.internalname)
        self.username = kwargs.get('username', config.get('username'))
        self.password = kwargs.get('password', config.get('password'))
        self.initsync = kwargs.get('initsync', self.base_config.startup.get('sync'))
        self.anonymous = bool(config.get('login', True))
        self.mirror = config.get('mirror', None)

    def stop(self):
        """
        Actions before service will be stopped.
        """
        logging.info("Service %s was disabled", self.name)

    def fetchUrl():
        raise NotImplementedError('This function must be implemented in subclass')

    def pushUrl(a):
        raise NotImplementedError('This function must be implemented in subclass')

    def save(self):
        """
        Only saves the current state to disk w/o network activity.
        """
        #self.local_db.set_db(self.db)
        pass

    def sync(self):
        """
        Syncronize local anime database with the service server.
        (fetch -> compare -> push -> update local)

        Return:
        nested dict of remote updates with ASCII-fied series titles as
        keys and a list of keys that got deleted on the service server.
        """
        # Three way switch: login (un)successfull or don't even try.
        if not self.anonymous and not self.login():
            logging.warn('Login to %s server failed..', self.name)
            return False

        # Get remote list and filter it
        (remote_updates, local_updates) = self.getList()
        self.logChanges(remote_updates, local_updates)
        if not self.anonymous:
            self.pushList(local_updates)
        else:
            logging.warn('Your local data goes ouf of sync')
        Anime.objects.save()

    def loadFile(self, filename):
        """
        Syncronize from given file.
        """
        #TODO: merge with sync
        remote_list = open(filename).read()
        remote_list = self.parseList(remote_list)
        (remote_updates, local_updates) = self.convertList(remote_list)
        self.logChanges(remote_updates, local_updates)
        Anime.objects.save()

    def sendRequest(self, link, data):
        try:
            response = self.opener.open(link, data)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                logging.error(u'Failed to reach %s server. Reason: %s',
                    self.name, e.reason)
            elif hasattr(e, 'code'):
                logging.error(u'The server couldn\'t fulfill the request. Error code %d',
                    e.code)
            return False
        return response

    def login(self):
        """
        Log in to service server.
        Returns: True on success, False on failure
        """
        raise NotImplementedError('Must be implemented in subclass')

    def getList(self):
        """
        Retrieve Anime list from service server and convert it to
        uniform local data format.
        Returns: dictionary object.
        """
        remote_list = self.fetchList()
        return self.convertList(self.parseList(remote_list))

    def fetchList(self):
        """
        Retrieve anime list from service server.
        Returns: remote data in its format.
        """
        fetch_response = self.opener.open(self.fetchURL())
        # TODO whatever error open raises.
        return unicode(fetch_response.read(), 'utf-8', 'replace')

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
        for item in recieved_list:
            decoded = self.decode(item)
            try:
                anime = Anime.objects.get(names__in=decoded['title'],
                                type=decoded['type'],
                                started=decoded.get('started', '*'))
            except DoesNotExists:
                anime = Anime(**decoded)
                anime.save()
                remote_updates.append(anime)
                continue
            updated = decoded.get('my_updated', datetime.now())
            if anime.my_updated < updated:
                remote_updates.append(anime)
                anime.update(decoded)
                anime.save()
            elif anime.my_updated > updated:
                local_updates.append(anime)
        return remote_updates, local_updates

    def decode(self, item, schema=None):
        """
        Convert item dictionary form remote service schema to local
        schema `db.models.LOCAL_ANIME_SCHEMA`. Service must provide
        convert list as schema parameter.
        Returns: converted dictionary
        """
        if not schema:
            raise NotImplementedError('Must be called with convert list')
        ret = {}
        for key, value in schema:
            if not key in item.keys():
                continue # Schema key not found, schema error maybe?
            if value in self.decodable_fields:
                ret[value] = self.decodeField(value, item[key])
            else:
                ret[value] = item[key]
        return ret

    def decodeField(self, name, value):
        """
        Make convert proceduer for specific fields
        """
        raise NotImplementedError('Must be implemented in subclass')

    def pushList(self, local_updates):
        """
        Updates every entry in the local updates dictionary to the server.
        Should be called after the local updates are determined with the
        _filterSyncChanges function.
        Returns:
            True on success, False on failure
        """
        for anime in local_updates:
            postdata = urllib.urlencode(self.makePost(anime))
            response = self.sendRequest(self.pushURL(anime), postdata)
            if not response:
                return False
            time.sleep(settings.TIMEOUT)
        return True

    def encodeList(self, sended_list):
        """
        Convert local list to service recieving format.
        Returns: dictionary object ready for posting to server.
        """
        raise NotImplementedError('Must be implemented in subclass')

    def logChanges(self, remote, local):
        """
        Writes changes to logfile.
        """
        for action, array in (('Fetching', remote), ('Pushing', local)):
            for anime in array:
                logging.info(u'{0} {1} episode {2}\n'.format(action,
                         anime.title, unicode(anime.my_episodes)))
