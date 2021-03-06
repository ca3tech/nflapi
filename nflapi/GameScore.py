import pandas
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.GameDataParser import GameDataParser

class GameScore(GameDataParser):

    def getGameScore(self, schedule_game : dict, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get game score for a given game
        
        This will use the gsis_id value in the input `schedule_game`
        to retrieve game scores.

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
        return self._process(schedule_game, return_type)

    def _doParse(self, srcdata : dict, basedata : dict) -> list:
        data = []
        for ttype in ["home", "away"]:
            tdata = srcdata[ttype]
            sdata : dict = basedata.copy()
            sdata.update({"team": tdata["abbr"],
                          "team_type": ttype})
            scoredata : dict = tdata["score"]
            for k, v in scoredata.items():
                try:
                    ki = int(k)
                    key = f"q{ki}"
                except ValueError:
                    key = "final"
                sdata[key] = v
            data.append(sdata)
        return data