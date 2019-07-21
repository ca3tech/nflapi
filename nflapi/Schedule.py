import os
from urllib3 import PoolManager
import pandas
import xml.sax
from nflapi.CachedAPI import CachedAPI, CachedRowFilter, ListOrDataFrame
from nflapi.ScheduleContentHandler import ScheduleContentHandler

class ScheduleRowFilter(CachedRowFilter):
    """Internal class used by the Schedule class
    
    This is used by the Schedule class to filter cached rows
    """
    def __init__(self, season : int, season_type : str, week : int):
        self._season = season
        self._season_type = season_type
        self._week = week

    def test(self, row : tuple) -> bool:
        return getattr(row, "season") == self._season and getattr(row, "season_type") == self._season_type and getattr(row, "week") == self._week

class Schedule(CachedAPI):
    """Retrieve game schedules

    This is used to retrieve the schedule of games for a given
    season, season type and week. The request may be for a
    past or future week.

    Methods
    -------
    getSchedule(season : int, season_type : str, week : int,
                return_type : ListOrDataFrame = list) -> ListOrDataFrame
    """

    def __init__(self):
        """Constructor for the Schedule class"""
        super(Schedule, self).__init__("http://www.nfl.com/ajax/scorestrip", ScheduleContentHandler())

    def getSchedule(self, season : int, season_type : str, week : int, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        """Retrieve games played or to be played for a given week
        
        This retrieves information about games played or to be
        played for a given week of the NFL season.

        Parameters
        ----------
        season : int
            The four digit year at the beginning of the NFL season
        season_type : str {"PRE", "REG", "POST"}
            PRE, for preseason, REG, for the regular season, or POST, for
            post-season
        week : int
            The week to retrieve data for. For PRE this is a number from 0 to 4.
            For REG this is a number from 1 to 17. For POST this is a number
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
        assert season_type in ["PRE", "REG", "POST"]
        wrng = range(1, 18)
        if season_type == "PRE":
            wrng = range(0, 5)
        elif season_type == "POST":
            wrng = range(1, 5)
        assert week in wrng

        if season_type == "POST":
            week += 17
            if week == 21:
                # The 21'st week is an off week between the conference final
                # and the super bowl. To allow the caller to not have to
                # know that we just add one more to the request.
                week += 1
        query = {"season": season, "seasonType": season_type, "week": week}
        rf = ScheduleRowFilter(season, season_type, week)
        return self._fetch(query, rf, return_type)
