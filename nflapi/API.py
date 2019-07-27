import xml.sax
from urllib3 import PoolManager
from bs4 import BeautifulSoup
from nflapi.AbstractContentHandler import AbstractContentHandler

class API(object):
    """Base class for classes that retrieve data from the NFL APIs"""

    def __init__(self, srcurl : str, handler : AbstractContentHandler):
        self._url = srcurl
        self._handler = handler
        self._http = PoolManager()

    def _queryAPI(self, query_doc : dict) -> str:
        rslt = self._http.request("GET", self._url, fields=query_doc)
        return rslt.data.decode("utf-8")

    def _parseDocument(self, docstr : str):
        xml.sax.parseString(docstr, self._handler)


