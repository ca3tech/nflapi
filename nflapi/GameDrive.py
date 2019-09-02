import pandas
import re
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.GameDataParser import GameDataParser
import nflapi.Utilities as util

class GameDrive(GameDataParser):

    def getGameDrive(self, schedule_game : dict, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get drive data for a given game
        
        This will use the gsis_id value in the input `schedule_game`
        to retrieve the drives for a game.

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
            # to a drive. If they child key is all numeric then
            # it does contain drive data.
            if re.search(r"^\d+$", driveid):
                ddata = basedata.copy()
                ddata["drive_id"] = driveid
                for dik, div in drive.items():
                    # We'll deal with plays elsewhere
                    if dik != "plays":
                        if dik in ["start", "end"]:
                            # The start and end values are dicts
                            # themselves, therefore we need to
                            # process each of its values.
                            for sek, sev in div.items():
                                ddata[f"{dik}_{sek}"] = sev
                        else:
                            ddata[dik] = div
                for kp in ["start", "end"]:
                    ylk = f"{kp}_yrdln"
                    # At the end of the game the end_yrdln may be
                    # blank. Since we don't actually know what the
                    # end position was we just don't record the
                    # normalized position.
                    if ddata[ylk] != "":
                        ydl = ddata[ylk]
                        if kp == "end" and ddata["result"] == "Touchdown":
                            # The end yrdln value in the data appears to be
                            # the last snap position that led to the touchdown.
                            # I would like the end_yrdln_norm - start_yrdln_norm - penyds
                            # to equal the ydsgained value so by overwritting
                            # the recorded value with "OPP 0" parseYardLine
                            # should return the desired result.
                            ydl = "OPP 0"
                        ddata[f"{ylk}_norm"] = util.parseYardLine(ydl, ddata["posteam"])
                data.append(ddata)
        return data