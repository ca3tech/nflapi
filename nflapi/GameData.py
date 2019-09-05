import json
from typing import List
from nflapi.CachedAPI import CachedAPI, CachedRowFilter, ListOrDataFrame

class GameDataRowFilter(CachedRowFilter):
    """Internal class used by the GameData class
    
    This is used by the GameData class to filter cached rows
    """
    def __init__(self, gsisid : str):
        self._gsisid = gsisid

    def test(self, row : dict) -> bool:
        return self._gsisid in row.keys()

class GameData(CachedAPI):
    __cache__ : List[dict] = []

    def __init__(self, use_shared_cache : bool = True):
        """Constructor for the GameData class
        
        Parameters
        ----------
        use_shared_cache : bool
            Should the shared GameData cache be used for the object [default: True]
        """
        super(GameData, self).__init__(None, None)
        if use_shared_cache:
            self._cache = GameData.__cache__
        self._url_base = "http://www.nfl.com/liveupdate/game-center/{gsisid}/{gsisid}_gtd.json"
        self._data : dict = None

    def getGameData(self, schedule_game : dict) -> List[dict]:
        gsisid = schedule_game["gsis_id"]
        # Set the URL which will be used by API._queryAPI
        self._url = self._url_base.format(gsisid=gsisid)
        return self._fetch(None, GameDataRowFilter(gsisid), list)

    def _parseDocument(self, docstr : str):
        self._data = json.loads(docstr)

    def _getResultList(self) -> List[dict]:
        return [self._data]
