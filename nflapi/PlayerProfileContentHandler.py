from bs4 import BeautifulSoup
import pandas
from nflapi.AbstractContentHandler import AbstractContentHandler
from nflapi.PlayerProfileBioFilter import PlayerProfileBioFilter
from nflapi.PlayerProfileInfoFilter import PlayerProfileInfoFilter
from nflapi.PlayerProfileInfoParser import PlayerProfileInfoParser

class PlayerProfileContentHandler(AbstractContentHandler):

    def __init__(self):
        self._data = []
    
    def parse(self, docstr : str):
        """Parse the playerprofile page for the player information
        
        Parameters
        ----------
        docstr : str
            The html document as a string
        """
        soup = BeautifulSoup(docstr, "html.parser")
        pbfilter = PlayerProfileBioFilter()
        pifilter = PlayerProfileInfoFilter()
        parser = PlayerProfileInfoParser()
        self._data = []
        for btag in soup.find_all(pbfilter.match):
            for itag in btag.find_all(pifilter.match):
                self._data.extend(parser.parse(itag))

    @property
    def list(self) -> list:
        return self._data

    @property
    def dataframe(self) -> pandas.DataFrame:
        return pandas.DataFrame(self.list)

    def mergeData(self, src : dict):
        """Add content from a dict to each data record
        
        Parameters
        ----------
        src : dict
            A dict containing data to be added to each
            of the data records
        """
        for d in self.list:
            d.update(src)