import pandas
import re
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.GameData import GameData

class GameDataParser(GameData):

    def _process(self, schedule_game : dict, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get game data parse it and return it
        
        This will use the gsis_id value in the input `schedule_game`
        to retrieve parsed game data.

        Parameters
        ----------
        schedule_game : dict
            A schedule game dictionary returned by `Schedule.getSchedule`
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list of dict or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        gdata = self.getGameData(schedule_game)
        # Game data is an atomic dict list.
        # The all numeric key of the dict is the gsis_id value for the game.
        gdkeys = [_ for _ in gdata[0].keys() if re.search(r"^\d+$", _)]
        gsisid = gdkeys[0]
        data = self._doParse(gdata[0][gsisid], {"gsis_id": gsisid})
        if return_type == pandas.DataFrame:
            data = pandas.DataFrame(data)
        return data

    def _doParse(self, srcdata : dict, basedata : dict) -> list:
        raise NotImplementedError("abstract base class GameDataParser method _doParse has not been implemented")
