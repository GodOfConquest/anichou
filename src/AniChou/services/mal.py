
import re
import urlparse
import urllib
import BeautifulSoup

from datetime import date, datetime
from AniChou.db.models import LOCAL_STATUS_R, LOCAL_TYPE_R
from AniChou.services.default import DefaultService
from AniChou.services.data import mal as data


class Mal(DefaultService):

    name = "myanimelist.net"
    decodable_fields = ('type', 'my_status', 'sources')

    def login(self):
        """
        Log in to MyAnimeList server.
        Returns: True on success, False on failure
        """
        # prepare login data
        login_url = 'http://myanimelist.net/login.php'
        login_data = urllib.urlencode({
                'username': self.username,
                'password': self.password,
                'cookie': 1,
                'sublogin': 'Login'})

        # try to connect and authenticate with MyAnimeList server
        login_response = self.sendRequest(login_url, login_data)
        if not login_response:
            return False

        login_response = login_response.read()

        # check if login was successful
        if not login_response.count('<div class="badresult">'):
            if login_response == "Couldn't open s-database. Please contact Xinil.":
                return False
            return True
        else:
            return False

    def fetchURL(self, status = 'all', typ = None):
        """
        Safely generate a URL to get XML.
        Type may be 'manga'.
        """
        # Example taken from the site.
        template = 'http://myanimelist.net/malappinfo.php?u=Wile&status=all&type=manga'
        # Make tuple mutable.
        parts = list(urlparse.urlparse(template))
        # New parameters.
        query = {'u': self.username}
        if status:
            query['status'] = status
        if typ:
            query['type'] = typ
        # urlencode would literally output 'None'.
        parts[4] = urllib.urlencode(query)
        return urlparse.urlunparse(parts)

    def parseList(self, fetch_response):
        """
        Process Anime XML from MyAnimeList server.
        Returns: dictionary object.
        Ways in which the ouput of malAppInfo is *not* XML:
        Declared as UTF-8 but contains illegal byte sequences (characters)
        Uses entities inside CDATA, which is exactly the wrong way round.
        It further disagrees with the Expat C extension behind minidom:
        Contains tabs and newlines outside of tags.
        """
        xmldata = BeautifulSoup.BeautifulStoneSoup(fetch_response)
        # For unknown reasons it doesn't work without recursive.
        # Nor does iterating over myanimelist.anime. BS documentation broken?
        anime_nodes = xmldata.myanimelist.findAll('anime', recursive = True)
        # We have to manually convert after getting them out of the CDATA.
        entity = lambda m: BeautifulSoup.Tag.XML_ENTITIES_TO_SPECIAL_CHARS[m.group(1)]
        # Walk through all the anime nodes and convert the data to a python
        # dictionary.
        ac_remote_anime_list = []
        for anime in anime_nodes:
            # ac_node builds the output of our function. Everything added to it
            # must either be made independent of the parse tree by calling
            # NavigableString.extract() or, preferrably, be turned into a
            # different type like unicode(). This is a side-effect of using
            # non-mutators like string.strip()
            # Failing to do this will crash cPickle.
            ac_node = dict()
            for node, typ in data.anime_schema.iteritems():
                try:
                    value = getattr(anime, node).string.strip()
                    # One would think re.sub directly accepts string subclasses
                    # like NavigableString. Raises a TypeError, though.
                    value = re.sub(r'&(\w+);', entity, value)
                except AttributeError:
                    continue
                if typ is datetime:
                    # process my_last_updated unix timestamp
                    ac_node[node] = datetime.fromtimestamp(int(value))
                elif typ is int:
                    # process integer slots
                    ac_node[node] = int(value)
                elif typ in (date, datetime):
                    if value != '0000-00-00':
                        try:
                            ac_node[node] = datetime.strptime(value, '%Y-%m-%d')
                            if typ is date:
                                ac_node[node] = ac_node[node].date()
                        except ValueError as e:
                            logging.warning('Error in parsing:\n{0}'.format(e))
                    else:
                        ac_node[node] = typ(1,1,1)
                else:
                    # process string slots
                    ac_node[node] = value

            # add node entry to the resulting nodelist
            ac_remote_anime_list.append(ac_node)

        # the resulting dict is like this:
        # [{<anime_data_schema-fields>: <values>}, ...]
        return ac_remote_anime_list

    def decode(self, item):
        return super(Mal, self).decode(item, data.anime_convert)

    def decodeField(self, name, value):
        if name == 'sources':
            return {self: value}
        elif name == 'type':
            return LOCAL_TYPE_R[value.lower()]
        elif name == 'my_status':
            return LOCAL_STATUS_R[value.lower()]
        return value

    def encode(self, item):
        return {}
