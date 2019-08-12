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
        pp = MockPlayerProfile(roster, "tests/data/profile_patrick_mahomes.html")
        exp = [{
            "first_name": "Patrick",
            "last_name": "Mahomes",
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
        self.assertEqual(pp.getProfile(list), exp)

    def test_getProfile_dataframe(self):
        roster = self.getRoster("patrickmahomes")
        pp = MockPlayerProfile(roster, "tests/data/profile_patrick_mahomes.html")
        exp = pandas.DataFrame([{
            "first_name": "Patrick",
            "last_name": "Mahomes",
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
        self.assertTrue(all(pp.getProfile(pandas.DataFrame).eq(exp)))

class MockPlayerProfile(PlayerProfile):
    def __init__(self, roster_data : dict, htmlpath : str):
        super(MockPlayerProfile, self).__init__(roster_data)
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

if __name__ == "__main__":
    unittest.main()




