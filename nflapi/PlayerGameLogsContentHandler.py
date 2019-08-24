from bs4 import BeautifulSoup
import pandas
from nflapi.AbstractContentHandler import AbstractContentHandler
from nflapi.PlayerGameLogsFilter import PlayerGameLogsFilter
from nflapi.PlayerGameLogsParser import PlayerGameLogsParser

class PlayerGameLogsContentHandler(AbstractContentHandler):

    def __init__(self, season : int = None):
        self._season = season
        self._data = []
    
    def parse(self, docstr : str):
        soup = BeautifulSoup(docstr, "html.parser")
        filter = PlayerGameLogsFilter()
        self._data = []
        for tag in soup.find_all(filter.match):
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
        for d in self.list:
            d.update(src)