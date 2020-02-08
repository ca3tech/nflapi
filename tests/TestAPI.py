import unittest
import pandas
from nflapi.API import API
from nflapi.AbstractContentHandler import AbstractContentHandler
from nflapi.Exceptions import MissingDocumentException

class TestAPI(unittest.TestCase):

    def test__processQuery_404(self):
        url = "http://httpstat.us/404"
        api = MockAPI(url, MockContentHandler())
        with self.assertRaisesRegex(MissingDocumentException, "document {} does not exist".format(url)):
            api._processQuery()

class MockAPI(API):

    def __init__(self, srcurl : str, handler : AbstractContentHandler):
        super(MockAPI, self).__init__(srcurl, handler)
        self._doc_string : str = None

    def getDocumentText(self) -> str:
        return self._doc_string

    def _parseDocument(self, docstr : str):
        self._doc_string = docstr

class MockContentHandler(AbstractContentHandler):

    @property
    def list(self) -> list:
        return []

    @property
    def dataframe(self) -> pandas.DataFrame:
        return pandas.DataFrame(self.list)
