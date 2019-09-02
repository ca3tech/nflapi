import unittest
import json
import pandas
from tests.MockGameData import MockGameData
from nflapi.GameSummary import GameSummary

class TestGameSummary(unittest.TestCase):
    def getSchedule(self, gsis_id : str) -> dict:
        with open("tests/data/schedule_2018_reg_16.json", "rt") as rfp:
            sch = json.load(rfp)
            il = [i for i in range(0, len(sch)) if sch[i]["gsis_id"] == gsis_id]
            return sch[il[0]]
    
    def test_getGameSummary_list(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122314_summary.json", "rt") as fp:
            exp = json.load(fp)
        gd = MockGameSummary("tests/data/game_2018122314_gtd.json")
        got = gd.getGameSummary(sch)
        self.assertEqual(got, exp)
    
    def test_getGameSummary_dataframe(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122314_summary.json", "rt") as fp:
            exp = pandas.DataFrame(json.load(fp))
        gd = MockGameSummary("tests/data/game_2018122314_gtd.json")
        got = gd.getGameSummary(sch, pandas.DataFrame)
        self.assertTrue(all(got.eq(exp)))
    
    def test_getGameSummary_2nd_call(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122313_summary.json", "rt") as fp:
            exp = json.load(fp)
        gd = MockGameSummary("tests/data/game_2018122314_gtd.json")
        got = gd.getGameSummary(sch)
        gsis_id = "2018122313"
        sch = self.getSchedule(gsis_id)
        gd.srcpath = "tests/data/game_2018122313_gtd.json"
        got = gd.getGameSummary(sch)
        self.assertEqual(got, exp)
    
class MockGameSummary(MockGameData, GameSummary):
    
    def __init__(self, srcpath : str):
        super(MockGameSummary, self).__init__(srcpath)
    