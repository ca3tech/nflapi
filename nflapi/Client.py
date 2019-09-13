from typing import List
import datetime
from dateutil import relativedelta
import pandas
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.Team import Team
from nflapi.Schedule import Schedule
import nflapi.Utilities as util

class Client:
    """Provides access to nfl.com data"""

    def __init__(self):
        self._schedule = Schedule()
        self._curdt = datetime.date.today()

    def getSchedule(self, season : int = None, season_type : str = None,
                    week : int = None, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve games played or to be played for a given week
        
        This retrieves information about games played or to be
        played for a given week of the NFL season.

        Parameters
        ----------
        season : int
            The four digit year at the beginning of the NFL season
        season_type : str {"preseason", "regular_season", "postseason"}
            preseason, for preseason, regular_season, for the regular season, or postseason, for
            post-season
        week : int
            The week to retrieve data for. For preseason this is a number from 0 to 4.
            For regular_season this is a number from 1 to 17. For postseason this is a number
            from 1 to 4.
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        sched = self._schedule
        rslt : list = []
        if season is not None and season_type is None and week is None:
            for st in ["preseason", "regular_season", "postseason"]:
                rslt.extend(self.getSchedule(season, st, return_type=list))
        elif season is not None and season_type is not None and week is None:
            if season_type == "preseason":
                si = 0
                ei = 5
            elif season_type == "postseason":
                si = 1
                ei = 5
            else:
                si = 1
                ei = 18
            for wk in range(si, ei):
                rslt.extend(self.getSchedule(season, season_type, wk, return_type=list))
        else:
            if season is None and season_type is None and week is None:
                season = self._currentSeason
                season_type = self._currentSeasonType
                week = self._currentWeek
                if week < 0:
                    week = 5 + week
            rslt = sched.getSchedule(season, season_type, week, return_type)
        if isinstance(return_type, pandas.DataFrame) and not isinstance(rslt, pandas.DataFrame):
            rslt = pandas.DataFrame(rslt)
        return rslt

    @property
    def _schedule(self) -> Schedule:
        return self._schedule_v

    @_schedule.setter
    def _schedule(self, nschedule : Schedule):
        self._schedule_v = nschedule

    @property
    def _currentDate(self) -> datetime.date:
        return self._curdt

    @property
    def _currentSeason(self) -> int:
        crdt = self._currentDate
        syear = crdt.year
        if crdt.month < 8:
            syear -= 1
        return syear

    @property
    def _currentSeasonType(self) -> str:
        week = self._currentWeek
        if week < 1:
            season_type = "preseason"
        elif week > 17:
            season_type = "postseason"
        else:
            season_type = "regular_season"
        return season_type

    @property
    def _seasonStartDate(self) -> datetime.date:
        syear = self._currentSeason
        # Get the first Thursday of Sept.
        rsstdt = util.getFirstDate(syear, 9, 3)
        # Get the first Monday of Sept.
        mon1dt = util.getFirstDate(syear, 9, 0)
        dt = datetime.date(syear, 9, 1) - mon1dt
        if dt.days > 0:
            # The 1st day of the month wasn't a Sunday or Monday
            # so the season starts on the 2nd Thursday
            rsstdt = rsstdt + relativedelta.relativedelta(weeks=1)
        return rsstdt

    @property
    def _currentWeek(self) -> int:
        crdt = self._currentDate
        ssdt = self._seasonStartDate - relativedelta.relativedelta(days=2)
        ddelta = crdt - ssdt
        week = 1
        if ddelta.days > 0:
            week = min(int(ddelta.days / 7) + 1, 22)
        elif ddelta.days < 0:
            week = max(int(ddelta.days / 7) - 1, -5)
        return week