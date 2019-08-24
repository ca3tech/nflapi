from bs4 import BeautifulSoup
import json
from nflapi.CachedAPI import CachedAPI, CachedRowFilter, ListOrDataFrame
from nflapi.PlayerGameLogsContentHandler import PlayerGameLogsContentHandler

class PlayerGameLogsRowFilter(CachedRowFilter):
    """Internal class used by the PlayerGameLogs class
    
    This is used by the PlayerGameLogs class to filter cached rows
    """
    def __init__(self, roster_data : dict, season : int):
        self._roster_data = roster_data
        self._season = season

    def test(self, row : dict) -> bool:
        x = False
        if "profile_id" in row.keys():
            x = row["profile_id"] == self._roster_data["profile_id"]
        if "season" in row.keys():
            x = x and row["season"] == self._season
        return x

class PlayerGameLogs(CachedAPI):

    def __init__(self):
        """Constructor for the PlayerGameLogs class"""
        super(PlayerGameLogs, self).__init__(None, PlayerGameLogsContentHandler())
    
    def getGameLogs(self, roster_data : dict, season : int, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get game logs (stats) for a player
        
        This will use the gamelogs URL in the input `roster_data`
        to retrieve game statistics for the provided season.

        Parameters
        ----------
        roster_data : dict
            A roster dictionary returned by `Roster.getRoster`
        season : int
            The season to retrieve data for
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list of dict or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        self._handler._season = season
        self._roster_data = roster_data
        return self._fetch({"season": season}, PlayerGameLogsRowFilter(self._roster_data, season), return_type)

    @property
    def _roster_data(self) -> dict:
        return self._roster_data_v

    @_roster_data.setter
    def _roster_data(self, roster_data : dict):
        assert not roster_data is None and "gamelogs_url" in roster_data.keys(), "roster_data contains no gamelogs_url"
        self._roster_data_v = roster_data
        self._url = roster_data["gamelogs_url"]

    def _parseDocument(self, docstr : str):
        self._handler.parse(docstr)
        pd = dict((k, self._roster_data[k]) for k in ["first_name", "last_name", "profile_id", "team"])
        self._handler.mergeData(pd)