import unittest
import json
import pandas
from nflapi.PlayerProfile import PlayerProfile

class TestPlayerProfile(unittest.TestCase):
    def getRoster(self, profile_name : str) -> str:
        with open("tests/data/roster_kc.json", "rt") as rfp:
            roster = json.load(rfp)
            il = [i for i in range(0, len(roster)) if roster[i]["profile_name"] == profile_name]
            return roster[il[0]]

    def test_getProfile_list(self):
        roster = self.getRoster("patrickmahomes")
        pp = MockPlayerProfile("tests/data/profile_patrick_mahomes.html")
        exp = [{
            "first_name": "Patrick",
            "last_name": "Mahomes",
            "number": 15,
            "position": "QB",
            "profile_id": 2558125,
            "team": "KC",
            "height": "6-3",
            "weight": 230,
            "age": 23,
            "born": "9/17/1995 Tyler, TX",
            "college": "Texas Tech",
            "experience": "3rd season",
            "high_school": "Whitehouse HS [TX]"
        }]
        self.assertEqual(pp.getProfile(roster, list), exp)

    def test_getProfile_dataframe(self):
        roster = self.getRoster("patrickmahomes")
        pp = MockPlayerProfile("tests/data/profile_patrick_mahomes.html")
        exp = pandas.DataFrame([{
            "first_name": "Patrick",
            "last_name": "Mahomes",
            "number": 15,
            "position": "QB",
            "profile_id": 2558125,
            "team": "KC",
            "height": "6-3",
            "weight": 230,
            "age": 23,
            "born": "9/17/1995 Tyler, TX",
            "college": "Texas Tech",
            "experience": "3rd season",
            "high_school": "Whitehouse HS [TX]"
        }])
        self.assertTrue(all(pp.getProfile(roster, pandas.DataFrame).eq(exp)))

    def test_getProfile_2nd_call_list(self):
        roster = self.getRoster("patrickmahomes")
        pp = MockPlayerProfile("tests/data/profile_patrick_mahomes.html")
        pp.getProfile(roster, list)
        self.assertEqual(pp.queryAPI_count, 1, "query count not expected after 1st call")
        roster = self.getRoster("tyreekhill")
        pp.htmlpath = "tests/data/profile_tyreek_hill.html"
        exp = [{
            "first_name": "Tyreek",
            "last_name": "Hill",
            "number": 10,
            "position": "WR",
            "profile_id": 2556214,
            "team": "KC",
            "height": "5-10",
            "weight": 185,
            "age": 25,
            "born": "3/1/1994 Lauderhill, FL",
            "college": "West Alabama",
            "experience": "4th season",
            "high_school": "Coffee Co. HS [Douglas, GA]"
        }]
        self.assertEqual(pp.getProfile(roster, list), exp)
        self.assertEqual(pp.queryAPI_count, 2, "query count not expected after 2nd call")

    def test_getProfile_uses_cache(self):
        roster = self.getRoster("patrickmahomes")
        pp = MockPlayerProfile("tests/data/profile_patrick_mahomes.html")
        pp.getProfile(roster, list)
        self.assertEqual(pp.queryAPI_count, 1, "query count not expected after 1st call")
        roster = self.getRoster("tyreekhill")
        pp.htmlpath = "tests/data/profile_tyreek_hill.html"
        pp.getProfile(roster, list)
        self.assertEqual(pp.queryAPI_count, 2, "query count not expected after 2nd call")
        roster = self.getRoster("patrickmahomes")
        pp.htmlpath = "tests/data/profile_patrick_mahomes.html"
        exp = [{
            "first_name": "Patrick",
            "last_name": "Mahomes",
            "number": 15,
            "position": "QB",
            "profile_id": 2558125,
            "team": "KC",
            "height": "6-3",
            "weight": 230,
            "age": 23,
            "born": "9/17/1995 Tyler, TX",
            "college": "Texas Tech",
            "experience": "3rd season",
            "high_school": "Whitehouse HS [TX]"
        }]
        self.assertEqual(pp.getProfile(roster, list), exp)
        self.assertEqual(pp.queryAPI_count, 2, "query count not expected after 3rd call")

    def test_getProfile_invalid_list(self):
        roster = self.getRoster("patrickmahomes")
        pp = MockPlayerProfile("tests/data/invalid_profile.html")
        self.assertEqual(pp.getProfile(roster, list), [])

class MockPlayerProfile(PlayerProfile):
    def __init__(self, htmlpath : str):
        super(MockPlayerProfile, self).__init__()
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




