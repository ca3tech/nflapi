import unittest
import json
import pandas
import datetime
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.Roster import Roster

class TestRoster(unittest.TestCase):

    def test_getRoster_one_team_list(self):
        obj = MockRoster("tests/data/roster_kc.html")
        rostd = obj.getRoster("KC")
        xrostd = getExpectedResults("tests/data/roster_kc.json")
        self.assertEqual(rostd, xrostd)

    def test_getRoster_one_team_dataframe(self):
        obj = MockRoster("tests/data/roster_kc.html")
        rostdf = obj.getRoster("KC", pandas.DataFrame)
        xrostdf = getExpectedResults("tests/data/roster_kc.json", pandas.DataFrame)
        self.assertTrue(all(rostdf.eq(xrostdf, axis="columns")), "data does not match")

    def test_getRoster_two_team_list(self):
        obj = MockRoster("tests/data/roster_pit.html")
        rostd = obj.getRoster("PIT")
        obj.htmlpath = "tests/data/roster_kc.html"
        rostd = obj.getRoster("KC")
        xrostd = getExpectedResults("tests/data/roster_kc.json")
        self.assertEqual(rostd, xrostd)
        
    @unittest.skip("enable to test hitting the nfl.com site")
    def test_getRoster_one_team_live(self):
        obj = Roster()
        rostd = obj.getRoster("KC")
        xrostd = getExpectedResults("tests/data/roster_kc_20191005.json")
        self.assertEqual(rostd, xrostd)

def getExpectedResults(jspath : str, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
    with open(jspath, "rt") as jfh:
        xschd = json.load(jfh)
        for i in range(0, len(xschd)):
            if xschd[i]["birthdate"] is not None:
                xschd[i]["birthdate"] = datetime.datetime.strptime(xschd[i]["birthdate"], "%m/%d/%Y")
    if issubclass(return_type, pandas.DataFrame):
        xschd = pandas.DataFrame(xschd)
    return xschd

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
        self._htmlpath = newpath
        with open(newpath, "rt") as fh:
            self._htmlstr = "".join(fh.readlines())

    def _queryAPI(self, query_doc : dict) -> str:
        self._qapi_count += 1
        return self._htmlstr

if __name__ == "__main__":
    unittest.main()




