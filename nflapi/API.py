import xml.sax
from urllib3 import PoolManager

class API(object):
    """Base class for classes that retrieve data from the NFL APIs"""

    def __init__(self, handler : xml.sax.ContentHandler):
        self._handler = handler
        self._http = PoolManager()

    def _queryAPI(self, srcurl : str, query_doc : dict) -> str:
        rslt = self._http.request("GET", srcurl, fields=query_doc)
        return rslt.data.decode("utf-8")

    def _parseXML(self, xmlstr):
        xml.sax.parseString(xmlstr, self._handler)


