import xml.sax
from urllib3 import PoolManager
from bs4 import BeautifulSoup
from nflapi.AbstractContentHandler import AbstractContentHandler

class API(object):
    """Base class for classes that retrieve data from the NFL APIs"""

    def __init__(self, srcurl : str, handler : AbstractContentHandler, content_type : str = "xml"):
        assert content_type in ["xml", "html"]
        self._url = srcurl
        self._handler = handler
        self._http = PoolManager()
        self._content_type = content_type

    def _queryAPI(self, query_doc : dict) -> str:
        rslt = self._http.request("GET", self._url, fields=query_doc)
        data = rslt.data.decode("utf-8")
        if self._content_type == "html":
            bs = BeautifulSoup(data, "html.parser")
            data = str(bs)
        return data

    def _parseXML(self, xmlstr):
        xml.sax.parseString(xmlstr, self._handler)


