from bs4 import BeautifulSoup
import json
from nflapi.CachedAPI import CachedAPI, CachedRowFilter, ListOrDataFrame
from nflapi.PlayerProfileContentHandler import PlayerProfileContentHandler

class PlayerProfileRowFilter(CachedRowFilter):
    """Internal class used by the PlayerProfile class
    
    This is used by the PlayerProfile class to filter cached rows
    """
    def __init__(self, roster_data : dict):
        self._roster_data = roster_data

    def test(self, row : dict) -> bool:
        x = False
        if "profile_id" in row.keys():
            x = row["profile_id"] == self._roster_data["profile_id"]
        return x

class PlayerProfile(CachedAPI):

    def __init__(self):
        """Constructor for the PlayerProfile class"""
        super(PlayerProfile, self).__init__(None, PlayerProfileContentHandler())
    
    def getProfile(self, roster_data : dict, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get the player profile
        
        This will use the profile_url of the provided roster record
        to retrieve the player profile.

        Parameters
        ----------
        roster_data : dict
            A record from the team roster data
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        self._roster_data = roster_data
        return self._fetch(None, PlayerProfileRowFilter(self._roster_data), return_type)

    @property
    def _roster_data(self) -> dict:
        return self._roster_data_v

    @_roster_data.setter
    def _roster_data(self, roster_data : dict):
        assert not roster_data is None and "profile_url" in roster_data.keys(), "roster_data contains no profile_url"
        self._roster_data_v = roster_data
        self._url = roster_data["profile_url"]

    def _parseDocument(self, docstr : str):
        # Parse the document with the handler
        self._handler.parse(docstr)
        # Add some of the data from the provided roster record to the profile data
        pd = dict((k, self._roster_data[k]) for k in ["first_name", "last_name", "profile_id", "team"])
        self._handler.mergeData(pd)