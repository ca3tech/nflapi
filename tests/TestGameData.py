import unittest
import json
from tests.MockGameData import MockGameData
from nflapi.GameData import GameData

class TestGameData(unittest.TestCase):
    def getSchedule(self, gsis_id : str) -> dict:
        with open("tests/data/schedule_2018_reg_16.json", "rt") as rfp:
            sch = json.load(rfp)
            il = [i for i in range(0, len(sch)) if sch[i]["gsis_id"] == gsis_id]
            return sch[il[0]]
    
    def test_getGameData(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        dfpath = "tests/data/game_2018122314_gtd.json"
        with open(dfpath, "rt") as fp:
            exp = [json.load(fp)]
        gd = MockGameData(dfpath)
        got = gd.getGameData(sch)
        self.assertEqual(gd._url, gd._url_base.format(gsisid=gsis_id), "URL not expected")
        self.assertEqual(got, exp)
    
    @unittest.skip("remove to test that we still work with what nfl.com returns")
    def test_getGameData_live(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        dfpath = "tests/data/game_2018122314_gtd.json"
        with open(dfpath, "rt") as fp:
            exp = [json.load(fp)]
        gd = GameData()
        got = gd.getGameData(sch)
        self.assertEqual(gd._url, gd._url_base.format(gsisid=gsis_id), "URL not expected")
        self.assertEqual(got, exp)
    
    def test_getGameData_2nd_call(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        dfpath = "tests/data/game_2018122314_gtd.json"
        gd = MockGameData(dfpath)
        got = gd.getGameData(sch)
        gsis_id = "2018122313"
        sch = self.getSchedule(gsis_id)
        dfpath = "tests/data/game_2018122313_gtd.json"
        gd.srcpath = dfpath
        got = gd.getGameData(sch)
        with open(dfpath, "rt") as fp:
            exp = [json.load(fp)]
        self.assertEqual(gd._url, gd._url_base.format(gsisid=gsis_id), "URL not expected")
        self.assertEqual(got, exp)
    
    def test_getGameData_cached(self):
        gsis_id1 = "2018122314"
        sch = self.getSchedule(gsis_id1)
        dfpath1 = "tests/data/game_2018122314_gtd.json"
        gd = MockGameData(dfpath1)
        got = gd.getGameData(sch)
        gsis_id2 = "2018122313"
        sch = self.getSchedule(gsis_id2)
        dfpath2 = "tests/data/game_2018122313_gtd.json"
        gd.srcpath = dfpath2
        got = gd.getGameData(sch)
        sch = self.getSchedule(gsis_id1)
        gd.srcpath = dfpath1
        got = gd.getGameData(sch)
        with open(dfpath1, "rt") as fp:
            exp = [json.load(fp)]
        self.assertEqual(gd._qapi_count, 2, "query count not expected")
        self.assertEqual(gd._url, gd._url_base.format(gsisid=gsis_id1), "URL not expected")
        self.assertEqual(got, exp)
