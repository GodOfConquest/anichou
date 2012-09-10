
import re
import urlparse
import urllib
import BeautifulSoup

from datetime import date, datetime
from AniChou.services.default import DefaultService
from AniChou.services.data.mal import mal_anime_data_schema


class Mal(DefaultService):

    name = "myanimelist.net"

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


    def getURL(self, user, status = 'all', typ = None):
        """
        Safely generate a URL to get XML.
        Type may be 'manga'.
        """
        # Example taken from the site.
        template = 'http://myanimelist.net/malappinfo.php?u=Wile&status=all&type=manga'
        # Make tuple mutable.
        parts = list(urlparse.urlparse(template))
        # New parameters.
        query = {'u': user}
        if status:
            query['status'] = status
        if typ:
            query['type'] = typ
        # urlencode would literally output 'None'.
        parts[4] = urllib.urlencode(query)
        return urlparse.urlunparse(parts)


    def recieveList(self):
        """
        Retrieve Anime XML from MyAnimeList server.
        Returns: dictionary object.
        Ways in which the ouput of malAppInfo is *not* XML:
        Declared as UTF-8 but contains illegal byte sequences (characters)
        Uses entities inside CDATA, which is exactly the wrong way round.
        It further disagrees with the Expat C extension behind minidom:
        Contains tabs and newlines outside of tags.
        """
        # This function should be broken up and partly refactored into
        # the class to be better configurable.
        fetch_url = self.getURL(self.username)
        try:
            fetch_response = open(self.mirror, 'rb')
        except:
            # TODO whatever error open(None) raises.
            fetch_response = self.opener.open(fetch_url)
        # BeautifulSoup could do the read() and unicode-conversion, if it
        # weren't for the illegal characters, as it internally doesn't
        # use 'replace'.
        fetch_response = unicode(fetch_response.read(), 'utf-8', 'replace')
        xmldata = BeautifulSoup.BeautifulStoneSoup(fetch_response)
        # For unknown reasons it doesn't work without recursive.
        # Nor does iterating over myanimelist.anime. BS documentation broken?
        anime_nodes = xmldata.myanimelist.findAll('anime', recursive = True)
        # We have to manually convert after getting them out of the CDATA.
        entity = lambda m: BeautifulSoup.Tag.XML_ENTITIES_TO_SPECIAL_CHARS[m.group(1)]
        # Walk through all the anime nodes and convert the data to a python
        # dictionary.
        ac_remote_anime_dict = dict()
        for anime in anime_nodes:
            # ac_node builds the output of our function. Everything added to it
            # must either be made independent of the parse tree by calling
            # NavigableString.extract() or, preferrably, be turned into a
            # different type like unicode(). This is a side-effect of using
            # non-mutators like string.strip()
            # Failing to do this will crash cPickle.
            ac_node = dict()
            for node, typ in mal_anime_data_schema.iteritems():
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
                elif typ is date and value != '0000-00-00':
                    # proces date slots
                    (y,m,d) = value.split('-')
                    (y,m,d) = int(y), int(m), int(d)
                    if y and m and d:
                        ac_node[node] = date(y,m,d)
                else:
                    # process string slots
                    ac_node[node] = value

            # series titles are used as anime identifiers
            # the keys for the resulting dictionary are encoded to ASCII, so they
            # can be simply put into shelves
            key = ac_node['series_title'].encode('utf-8')

            # add node entry to the resulting nodelist
            ac_remote_anime_dict[key] = ac_node

        # the resulting dict is like this:
        # {<ASCII-fied key from title>: {<mal_anime_data_schema-fields>: <values>}, ...}
        return ac_remote_anime_dict

    def decodeList(self, recieved_list):
        return {}

    def encodeList(self, sended_list):
        return {}
