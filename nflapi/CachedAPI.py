import os
from urllib3 import PoolManager
import pandas
from typing import TypeVar, List
from nflapi.API import API
from nflapi.AbstractContentHandler import AbstractContentHandler

ListOrDataFrame = TypeVar("ListOrDataFrame", list, pandas.DataFrame)

class CachedRowFilter(object):
    def test(self, row : dict) -> bool:
        raise NotImplementedError("abstract base class CachedRowFilter method test has not been implemented")

class CachedAPI(API):
    """
    Base class for classes that retrieve data from the NFL APIs where caching is desired
    """

    def __init__(self, srcurl : str, handler : AbstractContentHandler):
        super(CachedAPI, self).__init__(srcurl, handler)
        self._cache : List[dict] = None

    @property
    def _cache(self) -> List[dict]:
        return self._cache_v

    @_cache.setter
    def _cache(self, newcache : List[dict]) -> List[dict]:
        self._cache_v = newcache

    def _fetch(self, query : dict, row_filter : CachedRowFilter, return_type : ListOrDataFrame) -> ListOrDataFrame:
        """The main method of this class

        Subclasses should call this method to do their work. If the
        results of the query have not already been cached then this
        will call the objects _parseDocument method to process the
        query. It will then call the handler to retrieve the results
        to return to the caller.

        Parameters
        ----------
        query : dict
            Defines the query parameters for the API call if relevant.
            If not relevant then pass None.
        row_filter : CachedRowFilter
            This objects test method will be called to determine if a
            given cached row is should be returned.
        return_type : ListOrDataFrame
            The type of data to return; one of list or pandas.DataFrame

        Returns
        -------
        A list of dicts or pandas.DataFrame
        """
        if self._isInCache(row_filter):
            data = self._fromCache(row_filter, return_type)
        else:
            self._processQuery(query)
            # We expect the subclass to utilize the handler to
            # process the document, and therefore that we can
            # retrieve the results from the handler properties.
            data = self._getResultList()
            self._toCache(data)
            if return_type == pandas.DataFrame:
                data = self._getResultDataFrame()
        return data

    def _getResultDataFrame(self) -> pandas.DataFrame:
        return self._handler.dataframe

    def _getResultList(self) -> List[dict]:
        return self._handler.list

    def _isInCache(self, row_filter : CachedRowFilter) -> bool:
        # Use the provided row filter to determine if there
        # are rows in the cache meeting the query criteria
        cached = False
        if self._cache is not None:
            cached = any(self._getCacheRowVec(row_filter))
        return cached

    def _getCacheRowVec(self, row_filter : CachedRowFilter) -> list:
        # For each record in the cache use the provided row
        # filter to determine if the record is to be returned.
        # The returned value is a list of booleans of the
        # same length as the cache
        return [row_filter.test(row) for row in self._cache]

    def _toCache(self, data : List[dict]):
        if self._cache is None:
            self._cache = data
        else:
            self._cache.extend(data)

    def _fromCache(self, row_filter : CachedRowFilter, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        x = self._getCacheRowVec(row_filter)
        # Extract each row from the cache where the x value is True
        data = [self._cache[i] for i in range(0, len(self._cache)) if x[i]]
        if issubclass(return_type, pandas.DataFrame):
            data = pandas.DataFrame(data)
        return data
