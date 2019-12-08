from bs4 import BeautifulSoup, Tag
import pandas
from nflapi.AbstractContentHandler import AbstractContentHandler
from nflapi.PlayerGameLogsFilter import PlayerGameLogsFilter
from nflapi.PlayerGameLogsParser import PlayerGameLogsParser

class PlayerGameLogsContentHandler(AbstractContentHandler):

    def __init__(self, season : int = None):
        self._season = season
        self._data = []
    
    def parse(self, docstr : str):
        """Parse the gamelogs page for the player game data
        
        Parameters
        ----------
        docstr : str
            The html document as a string
        """
        soup = BeautifulSoup(docstr, "html.parser")
        filter = PlayerGameLogsFilter()
        self._data = []
        for tag in soup.find_all(filter.match):
            if tag.name == "select" and tag.has_attr("id") and tag["id"] == "season":
                sotags = tag.find_all(__selectedOptionFilter__)
                if len(sotags) > 0:
                    if int(sotags[0].string) != self._season:
                        self._data = []
                        break
            else:
                # Parse data from the current table tag
                parser = PlayerGameLogsParser(self._season)
                self._data.extend(parser.parse(tag))

    @property
    def _season(self) -> int:
        return self._ssn

    @_season.setter
    def _season(self, season : int):
        self._ssn = season

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

def __selectedOptionFilter__(tag : Tag) -> bool:
    return tag.name == "option" and tag.has_attr("selected")
