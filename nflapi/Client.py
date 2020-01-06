from typing import List
import datetime
from dateutil import relativedelta
import pandas
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.Team import Team
from nflapi.Schedule import Schedule
from nflapi.GameSummary import GameSummary
from nflapi.GameScore import GameScore
from nflapi.GamePlay import GamePlay
from nflapi.GameDrive import GameDrive
from nflapi.Team import Team
from nflapi.Roster import Roster
from nflapi.PlayerProfile import PlayerProfile
from nflapi.PlayerGameLogs import PlayerGameLogs
import nflapi.Utilities as util

class Client:
    """Provides access to nfl.com data
    
    This is the only module that you use directly as it
    provides access to all data available for the package.
    """

    def __init__(self):
        self._schedule = Schedule()
        self._gmsummary = GameSummary()
        self._gmscore = GameScore()
        self._gmplay = GamePlay()
        self._gmdrive = GameDrive()
        self._roster = Roster()
        self._plprof = PlayerProfile()
        self._plgmlog = PlayerGameLogs()
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
        return self._castReturnType(rslt, return_type)

    def getGameSummary(self, schedules : List[dict], return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve game summaries
        
        This retrieves game summaries for each game in the provide schedules

        Parameters
        ----------
        schedules : list of dict
            List of chedules as returned by `getSchedule` with return_type set to list
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        gsums : List[dict] = []
        for sched in schedules:
            gsums.extend(self._gmsummary.getGameSummary(sched, list))
        return self._castReturnType(gsums, return_type)

    def getGameScore(self, schedules : List[dict], return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve game scoring information
        
        This retrieves game scoring information for each game in the provide schedules

        Parameters
        ----------
        schedules : list of dict
            List of chedules as returned by `getSchedule` with return_type set to list
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        gscores : List[dict] = []
        for sched in schedules:
            gscores.extend(self._gmscore.getGameScore(sched, list))
        return self._castReturnType(gscores, return_type)

    def getGamePlay(self, schedules : List[dict], return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve play data for games
        
        This retrieves play data for each game in the provide schedules

        Parameters
        ----------
        schedules : list of dict
            List of chedules as returned by `getSchedule` with return_type set to list
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        gplays : List[dict] = []
        for sched in schedules:
            gplays.extend(self._gmplay.getGamePlay(sched, list))
        return self._castReturnType(gplays, return_type)

    def getGameDrive(self, schedules : List[dict], return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve drive data for games
        
        This retrieves drive data for each game in the provide schedules

        Parameters
        ----------
        schedules : list of dict
            List of chedules as returned by `getSchedule` with return_type set to list
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        gdrives : List[dict] = []
        for sched in schedules:
            gdrives.extend(self._gmdrive.getGameDrive(sched, list))
        return self._castReturnType(gdrives, return_type)

    def getTeams(self, active_only : bool = True, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Get the current teams
        
        This will return information about the teams in use by
        or formerly in use by nfl.com

        Parameters
        ----------
        active_only : bool
            If True then return teams that are currently in use; default True
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list of string
            The team abbreviations
        """
        teams = [Team(tabb) for tabb in Team.teams()]
        if active_only:
            teams = [t for t in teams if t.is_active]
        return self._castReturnType([t.__dict__ for t  in teams], return_type)

    def getRoster(self, teams : List[str], return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve team roster
        
        Retrieves profile information of players on the provided teams.
        You will usually want to pass list for the `return_type` as
        when that is the case the returned data can be used as parameter
        to other methods.

        Parameters
        ----------
        teams : list of str
            The team abbreviations for which to retrieve rosters.
            See `Client.getTeams` for the valid values.
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        rosters : List[dict] = []
        for team in teams:
            rosters.extend(self._roster.getRoster(team, list))
        return self._castReturnType(rosters, return_type)

    def getPlayerProfile(self, rosters : List[dict], return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve player profile information
        
        This retrieves player profile information for each item in the provided rosters

        Parameters
        ----------
        rosters : list of dict
            List of roster dicts as returned by `getRoster` with return_type set to list
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        profs : List[dict] = []
        for rost in rosters:
            profs.extend(self._plprof.getProfile(rost, list))
        return self._castReturnType(profs, return_type)

    def getPlayerGameLog(self, rosters : List[dict], season : int = None, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve player game logs
        
        This retrieves player game logs for the given season
        for each item in the provided rosters

        Parameters
        ----------
        rosters : list of dict
            List of roster dicts as returned by `getRoster` with return_type set to list
        season : int
            The season to retrieve data for. If not provided then game
            log data will be for the current season, or most recently
            completed season.
        return_type : list or pandas.DataFrame
            This defines the return type you would like. If the value is list
            then a list of dicts will be returned, if the value is pandas.DataFrame
            then a pandas.DataFrame will be returned. The default is list.

        Returns
        -------
        list or pandas.DataFrame
            Which type is returned is determined by the `return_type` parameter
        """
        if season is None:
            season = self._currentSeason
        gmlogs : List[dict] = []
        for rost in rosters:
            gmlogs.extend(self._plgmlog.getGameLogs(rost, season, list))
        return self._castReturnType(gmlogs, return_type)

    def _castReturnType(self, data : ListOrDataFrame, return_type : ListOrDataFrame) -> ListOrDataFrame:
        rslt = data
        if return_type == pandas.DataFrame and not isinstance(data, pandas.DataFrame):
            rslt = pandas.DataFrame(data)
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