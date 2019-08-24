import os
from urllib3 import PoolManager
from bs4 import BeautifulSoup, Tag
import pandas
from nflapi.CachedAPI import CachedAPI, CachedRowFilter, ListOrDataFrame
from nflapi.RosterContentHandler import RosterContentHandler
from nflapi.Team import Team

class RosterRowFilter(CachedRowFilter):
    """Internal class used by the Roster class
    
    This is used by the Roster class to filter cached rows
    """
    def __init__(self, team : str):
        self._team = team

    def test(self, row : dict) -> bool:
        x = False
        if "team" in row.keys():
            x = row["team"] == self._team
        return x

class Roster(CachedAPI):
    """Retrieve team rosters

    This is used to retrieve the player roster given team.

    Methods
    -------
    getRoster(team : str, return_type : ListOrDataFrame = list) -> ListOrDataFrame
    """
    
    def __init__(self):
        """Constructor for the Roster class"""
        super(Roster, self).__init__("http://www.nfl.com/teams/roster", RosterContentHandler())

    def getRoster(self, team : str, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve team roster
        
        This retrieves the profile information of players on a team.

        Parameters
        ----------
        team : str
            The team abbreviation to retrieve roster for
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        assert Team.is_team(team), f"team {team} is not valid"
        query = {"team": team}
        rf = RosterRowFilter(team)
        return self._fetch(query, rf, return_type)

    def _parseDocument(self, docstr : str):
        soup = BeautifulSoup(docstr, "html.parser")
        self._handler.startDocument()
        for tag in soup.find_all(["meta", "a"]):
            self._parseTag(tag)

    def _parseTag(self, tag : Tag):
        self._handler.startElement(tag.name, tag.attrs)
        if tag.name == "a":
            self._handler.characters(str(tag.string))
        self._handler.endElement(tag.name)