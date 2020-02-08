import xml.sax
from urllib3 import PoolManager, HTTPResponse
import re
from nflapi.AbstractContentHandler import AbstractContentHandler
from nflapi.Exceptions import MissingDocumentException

class API(object):
    """Base class for classes that retrieve data from the NFL APIs"""
    __http__ : PoolManager = PoolManager()

    def __init__(self, srcurl : str, handler : AbstractContentHandler):
        self._handler = handler
        self._http = API.__http__
        self._url = srcurl

    @property
    def _url(self) -> str:
        return self._srcurl

    @_url.setter
    def _url(self, srcurl : str):
        self._srcurl = srcurl

    def _processQuery(self, query_doc : dict = None):
        """Query nfl.com and process the results

        This will send the query to the nfl.com API/website
        and send the results to the `_parseDocument` method.
        """
        self._parseDocument(self._queryAPI(query_doc))

    def _queryAPI(self, query_doc : dict = None) -> str:
        rslt = self._http.request("GET", self._url, fields=query_doc)
        if rslt.status == 404:
            raise MissingDocumentException("document {} does not exist".format(self._url))
        return rslt.data.decode(self._getResponseEncoding(rslt))

    def _getResponseEncoding(self, response : HTTPResponse) -> str:
        enc = "utf-8"
        ctype = response.headers["Content-Type"]
        if re.search(r"charset=", ctype) is not None:
            enc = re.sub(r"^.+charset=", "", ctype)
        return enc

    def _parseDocument(self, docstr : str):
        """Implement this in your subclass
        
        The implementation should parse the given document text for
        the content of interest. This method returns nothing and so
        it is expected that the object will store the results
        internally for retrieval after this method call is complete.

        Parameters
        ----------
        docstr : str
            The document text to be parsed.
        """
        raise NotImplementedError("abstract base class API method _parseDocument has not been implemented")
