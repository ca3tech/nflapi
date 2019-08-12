import os
from urllib3 import PoolManager
import pandas
from typing import TypeVar
from nflapi.API import API
from nflapi.AbstractContentHandler import AbstractContentHandler

ListOrDataFrame = TypeVar("ListOrDataFrame", list, pandas.DataFrame)

class CachedRowFilter(object):
    def test(self, row : tuple) -> bool:
        raise NotImplementedError("abstract base class CachedRowFilter method test has not been implemented")

class CachedAPI(API):
    """
    Base class for classes that retrieve data from the NFL APIs where caching is desired
    """

    def __init__(self, srcurl : str, handler : AbstractContentHandler):
        super(CachedAPI, self).__init__(srcurl, handler)
        self._cache = None

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
            self._parseDocument(self._queryAPI(query))
            if issubclass(return_type, pandas.DataFrame):
                data = self._handler.dataframe
            else:
                data = self._handler.list
            self._toCache(data)
        return data

    def _isInCache(self, row_filter : CachedRowFilter) -> bool:
        cached = False
        if self._cache is not None:
            cached = any(self._getCacheRowVec(row_filter))
        return cached

    def _getCacheRowVec(self, row_filter : CachedRowFilter) -> list:
        return [row_filter.test(row) for row in self._cache.itertuples(index=False)]

    def _toCache(self, data : ListOrDataFrame):
        if issubclass(type(data), list):
            data = pandas.DataFrame(data)
        if self._cache is None:
            self._cache = data
        else:
            self._cache = self._cache.append(data, ignore_index=True)

    def _fromCache(self, row_filter : CachedRowFilter, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        x = self._getCacheRowVec(row_filter)
        data = self._cache[x]
        if issubclass(return_type, list):
            data = data.to_dict(orient="records")
        return data
