
import urllib2
from cookielib import LWPCookieJar

from AniChou.config import Config
from AniChou.database import db as local_database
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

    headers = {
        'User-Agent': u'Anichou {0}'.format(settings.VERSION),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    name = "Dummy service"

    def __init__(self, **kw):
        """
        Setup credentials, read local data and setup network connection
        environment. Optionally sync with MAL on startup.

        Does not take positional arguments. Keyword arguments can either be
        given individually (username, password, initsync) or as an
        ac_config() instance. This will not be retained.

        In the latter form we support some additional command line options.
        """
        # When the architecture stabilizes, switch to config as the sole
        # positional argument, and retain it instead of copying parts.
        # That would also enable reconfiguration at runtime.
        name = self.__class__.__name__
        self.base_config  = kw.get('config', Config())
        config = self.base_config.get(name, {})
        self.username = kw.get('username', config.get('username'))
        self.password = kw.get('password', config.get('password'))
        initsync      = kw.get('initsync', self.base_config.startup.get('sync'))
        self.anonymous = bool(config.get('login', True))
        self.mirror = config.get('mirror', None)

        # pull the local DB as a dictionary object
        #self.db = {}
        self.local_db = local_database()
        self.db = self.local_db.get_db()

        # setup cookie handler
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(LWPCookieJar()))
        urllib2.install_opener(opener)

        if initsync:
            self.sync()

    def stop(self):
        """
        Actions before service will be stopped.
        """
        print "Service {0} was disabled".format(self.name)

    def getUrl():
        raise NotImplementedError('This function must be implemented in subclass')

    def postUrl(a):
        raise NotImplementedError('This function must be implemented in subclass')

    def save(self):
        """
        Only saves the current state to disk w/o network activity.
        """
        self.local_db.set_db(self.db)

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
            print 'Login failed..'
            return False

        remoteAnime_db = self.getList()
        if self.db:
            # If local DB is already initialized then filter changes
            # and push local updates
            (remote_updates, local_updates, deleted_keys) = \
                self_filterSyncChanges(remoteAnime_db, self.db)
            self.logChanges(remote_updates, local_updates, deleted_keys)
            if not self.anonymous:
                self.pushList(local_updates)
            else:
                print 'Warning! Your local data goes ouf of sync'

            # update local anime list with changes
            for key in deleted_keys:
                del self.db[key]
            for key, value in remote_updates.items():
                self.db[key] = value

            # write to local DB
            self.local_db.set_db(self.db)

            return (remote_updates, deleted_entry_keys)
        else:
            # initialize local data, as it was empty before
            self.db = remoteAnime_db
            # write to local DB
            self.local_db.set_db(self.db)
            return (self.db, {})


    def fetch(self):
        """
        UNUSED
        Only fetch anime data from MyAnimeList server (overwrites local data,
        if existent). Useful for initializing and resetting local database.

        Returns a copy of the fetched database on success, None on failure.
        """
        self.db = _getAnimeList(self.username)
        # write to local DB
        self.local_db.set_db(self.db)
        return self.db


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
        recieved_list = self.recieveList()
        return self.decodeList(recieved_list)


    def recieveList(self):
        """
        Connect to server and get user list.
        Returns: anything you process in convertList method
        """
        raise NotImplementedError('Must be implemented in subclass')


    def decodeList(self, recieved_list):
        """
        Convert recieved service list to local format.
        Returns: dictionary object.
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
        for anime in local_updates.values():
            postdata = urllib.urlencode(self.makePost(anime))
            request = urllib2.Request(self.postURL(anime), postdata, self.headers)
            try:
                # push update request
                response = urllib2.urlopen(push_request)
            except URLError, e:
                if hasattr(e, 'reason'):
                    print u'We failed to reach a server.'
                    print u'Reason: ', unicode(e.reason)
                elif hasattr(e, 'code'):
                    print u'The server couldn\'t fulfill the request.'
                    print u'Error code: ', unicode(e.code)
                return False
            time.sleep(settings.TIMEOUT)
        return True


    def encodeList(self, sended_list):
        """
        Convert local list to service recieving format.
        Returns: dictionary object ready for posting to server.
        """
        raise NotImplementedError('Must be implemented in subclass')


    def _filterSyncChanges(self, remote_dict, local_dict):
        """
        Private Method
        Compares the anime entry status_updated in both parameters and returns two
        dictionaries of changed values of both parameters.

        Returns:
            remote_updates: changes that are more up to date on the server
            local_updates: changes that are more up to date locally
            deleted_enry_keys: keys that are in the local database, but not in the
                               remote list.
        """
        remote_updates = dict()
        local_updates = dict()

        # search for entirely new enries and deleted entries
        remote_keys = remote_dict.keys()
        local_keys = local_dict.keys()

        deleted_entry_keys = \
            filter(lambda x:x not in remote_keys, local_keys)

        new_entry_keys = \
            filter(lambda x:x not in local_keys, remote_keys)
        for key in new_entry_keys:
            remote_updates[key] = remote_dict[key]

        # search in both dictionaries for differing update keys and append to the
        # other's updates depending on which key is newer
        common_keys = filter(lambda x:x in local_keys, remote_keys)

        for key in common_keys:
            remote_timestamp = remote_dict[key]['status_updated']
            local_timestamp = local_dict[key]['status_updated']
            if remote_timestamp > local_timestamp:
                remote_updates[key] = remote_dict[key]
            elif remote_timestamp < local_timestamp:
                local_updates[key] = local_dict[key]

        return (remote_updates, local_updates, deleted_entry_keys)


    def logChanges(remote, local, deleted):
        """
        Writes changes to logfile.
        """
        f = open(settings.LOG_PATH, 'a')
        now = str(int(time.mktime(datetime.now().timetuple())))
        for key, value in remote.items():
            f.write(u'[{0}] Fetching {1} episode {2}\n'.format(
                    now, key, unicode(value['status_episodes'])))
        for key, value in local.items():
            f.write(u'[{0}] Pushing {1} episode {2}\n'.format(
                    now, key, unicode(value['status_episodes'])))
        for entry in deleted:
            f.write(u'[{0}] Deleted "{1}"\n'.format(now, entry))
        f.close()
