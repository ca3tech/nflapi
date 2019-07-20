import os
from urllib3 import PoolManager
import pandas
import xml.sax
from typing import TypeVar
from nflapi.ScheduleContentHandler import ScheduleContentHandler

ListOrDataFrame = TypeVar("ListOrDataFrame", list, pandas.DataFrame)

class Schedule(object):
    """
    Retrieve game schedules
    """

    _url : str = "http://www.nfl.com/ajax/scorestrip"

    def __init__(self):
        self._cache = None
        self._handler = ScheduleContentHandler()
        self._http = PoolManager()

    def getSchedule(self, season : int, season_type : str, week : int, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        data = None
        if self._isInCache(season, season_type, week):
            data = self._fromCache(season, season_type, week, return_type)
        else:
            self._queryAndParse(season, season_type, week)
            if issubclass(return_type, pandas.DataFrame):
                data = self._handler.dataframe
            else:
                data = self._handler.list
            self._toCache(data)
        return data
   
    def _queryAndParse(self, season : int, season_type : str, week : int):
        xmlstr = self._queryAPI(Schedule._url, {"season": season, "seasonType": season_type, "week": week})
        self._parseXML(xmlstr)

    def _queryAPI(self, srcurl : str, query_doc : dict) -> str:
        rslt = self._http.request("GET", srcurl, fields=query_doc)
        return rslt.data.decode("utf-8")

    def _parseXML(self, xmlstr):
        xml.sax.parseString(xmlstr, self._handler)

    def _isInCache(self, season : int, season_type : str, week : int) -> bool:
        cached = False
        if self._cache is not None:
            cached = any(self._getCacheRowVec(season, season_type, week))
        return cached

    def _getCacheRowVec(self, season : int, season_type : str, week : int) -> list:
        return [getattr(row, "season") == season and getattr(row, "season_type") == season_type and getattr(row, "week") == week for row in self._cache.itertuples(index=False)]

    def _toCache(self, data : ListOrDataFrame):
        if issubclass(type(data), list):
            data = pandas.DataFrame(data)
        if self._cache is None:
            self._cache = data
        else:
            self._cache = self._cache.append(data, ignore_index=True)

    def _fromCache(self, season : int, season_type : str, week : int, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        x = self._getCacheRowVec(season, season_type, week)
        data = self._cache[x]
        if issubclass(return_type, list):
            data = data.to_dict(orient="records")
        return data
