
import base64
import json
import re
import urlparse
import urllib
import BeautifulSoup

from datetime import date, datetime
from AniChou.db.data import LOCAL_STATUS_R, LOCAL_TYPE_R, LOCAL_AIR_R
from AniChou.services.default import DefaultService
from AniChou.services.data import mal as data


class Mal(DefaultService):

    name = "myanimelist.net"
    decode_schema = data.anime_convert

    def login(self):
        """
        This function checks credentials on the server and setup
        authorization header.
        Returns: True on success, False on failure.
        """
        # prepare login data

        login_url = 'http://mal-api.com/account/verify_credentials'
        headers = filter(lambda hdr: hdr[0] != 'Authorization', self.opener.addheaders)

        encoded = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        headers.append(('Authorization', 'Basic %s' % encoded))

        self.opener.addheaders = headers

        # try to check credentials on server
        login_response = self.sendRequest(login_url)

        if login_response and getattr(login_response, 'code', 0) == 200:
            return True

        return False

    def fetchURL(self):
        """
        Safely generate a URL to get list.
        """
        return 'http://mal-api.com/animelist/{0}'.format(self.username)

    def parseList(self, fetch_response):
        """
        Process Anime from MyAnimeList server.
        Check if it is a json or xml and use correct processor.
        Returns: dictionary object.
        """
        try:
            return self.parseJSON(fetch_response)
        except IOError:
            return self.parseXML(fetch_response)

    def parseJSON(self, fetch_response):
        """
        Process Anime json object from MyAnimeList server.
        Returns: list of dictionary objects.
        """
        try:
            anime_nodes = json.loads(fetch_response)
        except ValueError as e:
            raise IOError('Not a json:\n{0}'.format(e))

        ac_remote_anime_list = []
        for anime in anime_nodes.get('anime', {}):
            ac_node = {}
            for node, local_node in data.anime_convert_json_default:
                typ = data.anime_schema.get(local_node)
                if not typ:
                    continue
                value = anime.get(node)
                ac_node[local_node] = self.parseNode(value, typ)
            # add node entry to the resulting nodelist
            ac_remote_anime_list.append(ac_node)
        return ac_remote_anime_list

    def parseXML(self, fetch_response):
        """
        Process Anime XML from MyAnimeList server.
        Returns: list of dictionary objects.
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
                ac_node[node] = self.parseNode(value, typ)
            # add node entry to the resulting nodelist
            ac_remote_anime_list.append(ac_node)

        # the resulting dict is like this:
        # [{<anime_data_schema-fields>: <values>}, ...]
        return ac_remote_anime_list

    def parseNode(self, value, typ):
        if typ is datetime:
            # process my_last_updated unix timestamp
            ac_node = datetime.fromtimestamp(int(value))
        elif typ is int:
            # process integer slots
            ac_node = int(value)
        elif typ in (date, datetime):
            if value and value != '0000-00-00':
                try:
                    ac_node = datetime.strptime(value, '%Y-%m-%d')
                    if typ is date:
                        ac_node = ac_node.date()
                except ValueError as e:
                    logging.warning('Error in parsing:\n{0}'.format(e))
            else:
                ac_node = typ(1,1,1)
        else:
            # process string slots
            ac_node = value
        return ac_node

    def decodeField(self, name, value):
        if name == 'sources':
            return {self: value}
        elif name == 'type':
            return LOCAL_TYPE_R[value.lower()]
        elif name == 'my_status':
            return LOCAL_STATUS_R[value.lower()]
        elif name == 'air':
            return LOCAL_AIR_R[value.lower()]
        return value

    def encode(self, item):
        return {}
