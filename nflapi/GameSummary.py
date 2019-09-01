import pandas
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.GameDataParser import GameDataParser

class GameSummary(GameDataParser):

    def getGameSummary(self, schedule_game : dict, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get game summary for a given game
        
        This will use the gsis_id value in the input `schedule_game`
        to retrieve the game summary. The game summary consists of
        the overall game statistics for players and the team.

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
            statdata : dict = tdata["stats"]
            for grpname, grpdict in statdata.items():
                if grpname == "team":
                    datum = sdata.copy()
                    for k, v in grpdict.items():
                        datum[f"{grpname}_{k}"] = v
                    data.append(datum)
                else:
                    for plid, pldict in grpdict.items():
                        datum = sdata.copy()
                        datum["player_id"] = plid
                        datum["player_abrv_name"] = pldict["name"]
                        for statname in [_ for _ in pldict.keys() if _ != "name"]:
                            datum[f"{grpname}_{statname}"] = pldict[statname]
                        data.append(datum)
        return data