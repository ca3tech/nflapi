from bs4 import BeautifulSoup, Tag
import pandas
from nflapi.AbstractContentHandler import AbstractContentHandler
from nflapi.BSTagFilter import BSTagFilter
from nflapi.RosterParser import RosterParser

class RosterFilter(BSTagFilter):
    def match(self, tag : Tag) -> bool:
        return (tag.name == "table"
                and tag.has_attr("class") and tag["class"] == ["data-table1"]
                and tag.has_attr("id") and tag["id"] == "result")

class RosterContentHandler(AbstractContentHandler):

    def __init__(self, team : str = None, domain : str = "http://www.nfl.com"):
        self._domain = domain
        self._team = team
        self._data = []

    @property
    def team(self) -> str:
        return self._team

    @team.setter
    def team(self, newteam : str):
        self._team = newteam
    
    def parse(self, docstr : str):
        """Parse the team roster page
        
        Parameters
        ----------
        docstr : str
            The html document as a string
        """
        soup = BeautifulSoup(docstr, "html.parser")
        filter = RosterFilter()
        tags = soup.find_all(filter.match)
        # Parse data from the table tag
        parser = RosterParser(self._domain, self._team)
        self._data = parser.parse(tags[0])

    @property
    def _domain(self) -> int:
        return self._dmn

    @_domain.setter
    def _domain(self, domain : int):
        self._dmn = domain

    @property
    def list(self) -> list:
        return self._data

    @property
    def dataframe(self) -> pandas.DataFrame:
        return pandas.DataFrame(self.list)
