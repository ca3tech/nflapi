import pandas
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.GameData import GameData

class GameScore(GameData):

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
        gdata = self.getGameData(schedule_game)
        gdkeys = [_ for _ in gdata[0].keys()]
        gsisid = gdkeys[0]
        data = []
        for ttype in ["home", "away"]:
            tdata = gdata[0][gsisid][ttype]
            sdata = {
                "gsis_id": gsisid,
                "team": tdata["abbr"],
                "team_type": ttype
            }
            srcdata : dict = tdata["score"]
            for k, v in srcdata.items():
                try:
                    ki = int(k)
                    key = f"q{ki}"
                except ValueError:
                    key = "final"
                sdata[key] = v
            data.append(sdata)
        if issubclass(return_type, pandas.DataFrame):
            data = pandas.DataFrame(data)
        return data