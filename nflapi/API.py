import xml.sax
from urllib3 import PoolManager
from nflapi.AbstractContentHandler import AbstractContentHandler

class API(object):
    """Base class for classes that retrieve data from the NFL APIs
    
    TODO:
    -----
    Investigate making this threaded. Perhaps make it extend Thread.
    """
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

    def _queryAPI(self, query_doc : dict = None) -> str:
        rslt = self._http.request("GET", self._url, fields=query_doc)
        return rslt.data.decode("utf-8")

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
