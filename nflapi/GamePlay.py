import pandas
import re
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.GameDataParser import GameDataParser
import nflapi.Utilities as util
import nflgame.statmap as sm

class GamePlay(GameDataParser):

    def getGamePlay(self, schedule_game : dict, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get play data for a given game
        
        This will use the gsis_id value in the input `schedule_game`
        to retrieve the play data for a game.

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
        for driveid, drive in srcdata["drives"].items():
            # The drive contains children that do not correspond
            # to a drive. If the child key is all numeric then
            # it does contain drive data.
            if re.search(r"^\d+$", driveid):
                for dik, div in drive.items():
                    if dik == "plays":
                        # div is the plays dict which contains
                        # the data we want
                        for playid, playdict in div.items():
                            ddata = basedata.copy()
                            ddata["drive_id"] = driveid
                            ddata["play_id"] = playid
                            for pk, pv in playdict.items():
                                if pk != "players":
                                    # This is an atomic valued element
                                    # so just add it as-is
                                    ddata[pk] = pv
                            if ddata["yrdln"] != "":
                                # We need to get a normalized yardline like we
                                # do in the game summary data.
                                ddata["yrdln_norm"] = util.parseYardLine(ddata["yrdln"], ddata["posteam"])
                            if "players" in playdict.keys():
                                # We have player statistics listed, therefore, we need
                                # to add a record for each player statistic
                                for pldata in self._doPlayerParse(playdict["players"], ddata):
                                    data.append(pldata)
                            else:
                                # No player statistics listed so just add the base record
                                data.append(ddata)
        return data

    def _doPlayerParse(self, srcdata : dict, basedata : dict) -> list:
        data = []
        for playerid, pllist in srcdata.items():
            for plitem in pllist:
                pdata = basedata.copy()
                pdata["player_id"] = playerid
                data.append(self._doPlayerItemParse(plitem, pdata))
        return data

    def _doPlayerItemParse(self, srcdata : dict, basedata : dict) -> dict:
        data = basedata.copy()
        for k, v in srcdata.items():
            if k != "yards":
                # Ignore the yards key at this level
                k = re.sub(r"([a-z])([A-Z])", r"\1_\2", k)
                k = k.lower()
                if k == "stat_id":
                    # Now we use the yards value in the srcdata
                    # Add the statistic flags and the statistic yardage value
                    vd = sm.values(v, srcdata["yards"])
                    # Add the statistic metadata
                    vd.update(util.getStatMetadata(v))
                    data.update(vd)
                else:
                    if k == "player_name":
                        k = "player_abrv_name"
                    elif k == "clubcode":
                        k = "team"
                    data[k] = v
        return data