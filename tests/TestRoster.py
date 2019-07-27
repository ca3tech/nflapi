import unittest
import json
import pandas
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.Roster import Roster

class TestRoster(unittest.TestCase):

    def getExpectedResults(self, jspath : str, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
        with open(jspath, "rt") as jfh:
            xrostd = json.load(jfh)
        if issubclass(return_type, pandas.DataFrame):
            xrostd = pandas.DataFrame(xrostd)
        return xrostd

    def test_getRoster_one_team_list(self):
        obj = MockRoster("tests/data/roster_kc.html")
        rostd = obj.getRoster("KC")
        xrostd = self.getExpectedResults("tests/data/roster_kc.json")
        self.assertEqual(rostd, xrostd)

    def test_getRoster_one_team_dataframe(self):
        obj = MockRoster("tests/data/roster_kc.html")
        rostdf = obj.getRoster("KC", pandas.DataFrame)
        xrostdf = self.getExpectedResults("tests/data/roster_kc.json", pandas.DataFrame)
        self.assertTrue(all(rostdf.eq(xrostdf, axis="columns")), "data does not match")

    def test_getRoster_two_team_list(self):
        obj = MockRoster("tests/data/roster_pit.html")
        rostd = obj.getRoster("PIT")
        obj.htmlpath = "tests/data/roster_kc.html"
        rostd = obj.getRoster("KC")
        xrostd = self.getExpectedResults("tests/data/roster_kc.json")
        self.assertEqual(rostd, xrostd)
        
    @unittest.skip("unset to run test that actually hits the nfl api")
    def test_getRoster_one_team_live(self):
        obj = Roster()
        rostd = obj.getRoster("KC")
        xrostd = self.getExpectedResults("tests/data/roster_kc_20190727.json")
        self.assertEqual(rostd, xrostd)

class MockRoster(Roster):
    def __init__(self, htmlpath : str):
        super(MockRoster, self).__init__()
        self.htmlpath = htmlpath
        self._qapi_count = 0

    @property
    def queryAPI_count(self):
        return self._qapi_count

    @property
    def htmlpath(self) -> str:
        return self._htmlpath

    @htmlpath.setter
    def htmlpath(self, newpath):
        with open(newpath, "rt") as fh:
            self._htmlstr = "".join(fh.readlines())

    def _queryAPI(self, query_doc : dict) -> str:
        self._qapi_count += 1
        return self._htmlstr




