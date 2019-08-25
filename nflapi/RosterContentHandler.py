import re
import xml.sax
import pandas
from nflapi.AbstractContentHandler import AbstractContentHandler

class RosterContentHandler(AbstractContentHandler, xml.sax.ContentHandler):
    """Parse player profile data from NFL team roster page
    
    Consumes tags like:
        team name: <meta id='teamName' content='KC' />
        player: <a href="/player/patrickmahomes/2558125/profile">Mahomes, Patrick</a></td>
    """

    def __init__(self, domain="http://www.nfl.com"):
        """Create a new RosterContentHandler object"""
        self._domain = domain
        self._reset()

    def startDocument(self):
        """Indicate that document processing is beginning"""
        
        # We reset our data so as to not be tainted by previous uses of the handler
        self._reset()

    def startElement(self, name : str, attrs : dict):
        """Called when processing of a tag begins
        
        Parameters
        ----------
        name : str
            The name of the tag
        attrs : dict
            A dict of attributes associated with the tag
        """
        if name == "meta" and "id" in attrs.keys() and attrs["id"] == "teamName":
            # The content attribute contains the team name
            self._team = attrs["content"]
        elif name == "a" and re.search(r"player.+profile", attrs["href"]):
            # The href attribute of the tag contains the player profile URL
            # Extract information from the URL and assign the data to
            # the _processing_profile attribute so that it is available
            # to other methods.
            self._processing_profile = self._parse_profile(attrs)

    def endElement(self, name : str):
        """Called when processing of a tag ends
        
        Parameters
        ----------
        name : str
            The name of the tag
        """
        if name == "a" and self._processing_profile is not None:
            # We have been processing a tag containing player
            # profile information, therefore, we add the data
            self._data.append(self._processing_profile)
            self._processing_profile = None

    def characters(self, content : str):
        """Called when current element contains text"""
        if self._processing_profile is not None:
            # We are processing a player profile tag and it
            # text value should look like "{last name}, {first name}".
            # If it does then we add the last and first
            # name to the current _processing_profile.
            m = re.search(r"^([^\,]+)\,\s*(.+)$", content)
            if m is not None:
                self._processing_profile["last_name"] = m.group(1)
                self._processing_profile["first_name"] = m.group(2)

    @property
    def list(self) -> list:
        return self._data.copy()

    @property
    def dataframe(self) -> pandas.DataFrame:
        return pandas.DataFrame(self.list)

    def _reset(self):
        self._team = None
        self._data = []
        self._processing_profile = None

    def _parse_profile(self, attrs : dict) -> dict:
        m = re.search(r"player/([^/]+)/(\d+)/profile", attrs["href"])
        d = {}
        if m is not None:
            # Prefix the domain to the URL as it is relative
            purl = "{}{}".format(self._domain, attrs["href"])
            csurl = purl.replace("profile", "careerstats")
            gsurl = purl.replace("profile", "gamesplits")
            glurl = purl.replace("profile", "gamelogs")
            d = {"profile_id": int(m.group(2)),
                 "profile_name": m.group(1),
                 "profile_url": purl,
                 "careerstats_url": csurl,
                 "gamelogs_url": glurl,
                 "gamesplits_url": gsurl}
            if self._team is not None:
                d["team"] = self._team
        return d