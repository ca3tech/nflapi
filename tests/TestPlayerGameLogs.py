import unittest
import json
import pandas
import time
from nflapi.PlayerGameLogs import PlayerGameLogs

class TestPlayerGameLogs(unittest.TestCase):
    def getRoster(self, profile_name : str) -> str:
        with open("tests/data/roster_kc.json", "rt") as rfp:
            roster = json.load(rfp)
            il = [i for i in range(0, len(roster)) if roster[i]["profile_name"] == profile_name]
            return roster[il[0]]
    
    def getExpectedList(self, fpath : str = "tests/data/gamelogs_patrick_mahomes_2018.json"):
        with open(fpath, "rt") as fp:
            recs = json.load(fp)
        for i in range(0, len(recs)):
            recs[i]["game_date"] = time.struct_time(recs[i]["game_date"])
        return recs

    def assertDictListEqual(self, rslt : list, exp : list):
        x = len(rslt) == len(exp)
        self.assertTrue(x, "list lengths differ")
        if x:
            for i in range(0, len(rslt)):
                rrec : dict = rslt[i]
                xrec : dict = exp[i]
                xrk = [k for k in rrec.keys() if k not in xrec.keys()]
                xxk = [k for k in xrec.keys() if k not in rrec.keys()]
                x = len(xrk) == 0 and len(xxk) == 0
                if x:
                    for k in rrec.keys():
                        self.assertEqual(rrec[k], xrec[k], f"rec {i} key {k} differs")
                else:
                    xrk.sort()
                    xxk.sort()
                    self.assertTrue(x, f"rec {i} keys differ ({','.join(xrk)}) ({','.join(xxk)})")

    def test_getGameLogs_list(self):
        roster = self.getRoster("patrickmahomes")
        pgl = MockPlayerGameLogs("tests/data/gamelogs_patrick_mahomes_2018.html")
        got = pgl.getGameLogs(roster, 2018, list)
        exp = self.getExpectedList()
        self.assertEqual(got, exp)

    def test_getGameLogs_dataframe(self):
        roster = self.getRoster("patrickmahomes")
        pgl = MockPlayerGameLogs("tests/data/gamelogs_patrick_mahomes_2018.html")
        got = pgl.getGameLogs(roster, 2018, pandas.DataFrame)
        exp = pandas.DataFrame(self.getExpectedList())
        self.assertTrue(all(got.eq(exp)))

    def test_getGameLogs_2nd_call_list(self):
        roster = self.getRoster("patrickmahomes")
        pgl = MockPlayerGameLogs("tests/data/gamelogs_patrick_mahomes_2018.html")
        got = pgl.getGameLogs(roster, 2018, list)
        roster = self.getRoster("tyreekhill")
        pgl.htmlpath = "tests/data/gamelogs_tyreek_hill_2018.html"
        got = pgl.getGameLogs(roster, 2018, list)
        exp = self.getExpectedList("tests/data/gamelogs_tyreek_hill_2018.json")
        self.assertEqual(pgl._qapi_count, 2, "query count not expected")
        self.assertEqual(got, exp, "data not expected")

    def test_getGameLogs_uses_cache(self):
        pmhtml = "tests/data/gamelogs_patrick_mahomes_2018.html"
        pmroster = self.getRoster("patrickmahomes")
        pgl = MockPlayerGameLogs(pmhtml)
        got = pgl.getGameLogs(pmroster, 2018, list)
        roster = self.getRoster("tyreekhill")
        pgl.htmlpath = "tests/data/gamelogs_tyreek_hill_2018.html"
        got = pgl.getGameLogs(roster, 2018, list)
        pgl.htmlpath = pmhtml
        got = pgl.getGameLogs(pmroster, 2018, list)
        exp = self.getExpectedList()
        self.assertEqual(pgl._qapi_count, 2, "query count not expected")
        self.assertDictListEqual(got, exp)

class MockPlayerGameLogs(PlayerGameLogs):
    def __init__(self, htmlpath : str):
        super(MockPlayerGameLogs, self).__init__()
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
