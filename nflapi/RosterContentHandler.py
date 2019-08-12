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
        # This is called by the sax parser when it first starts processing a document
        # We reset our data so as to not be tainted by previous uses of the handler
        self._reset()

    def startElement(self, name : str, attrs : dict):
        if name == "meta" and "id" in attrs.keys() and attrs["id"] == "teamName":
            self._team = attrs["content"]
        elif name == "a" and re.search(r"player.+profile", attrs["href"]):
            self._processing_profile = self._parse_profile(attrs)

    def endElement(self, name : str):
        if name == "a" and self._processing_profile is not None:
            self._data.append(self._processing_profile)
            self._processing_profile = None

    def characters(self, content : str):
        if self._processing_profile is not None:
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