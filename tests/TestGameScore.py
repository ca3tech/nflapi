import unittest
import json
import pandas
from tests.MockGameData import MockGameData
from nflapi.GameScore import GameScore

class TestGameScore(unittest.TestCase):
    def getSchedule(self, gsis_id : str) -> dict:
        with open("tests/data/schedule_2018_reg_16.json", "rt") as rfp:
            sch = json.load(rfp)
            il = [i for i in range(0, len(sch)) if sch[i]["gsis_id"] == gsis_id]
            return sch[il[0]]
    
    def test_getGameScore_list(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122314_score.json", "rt") as fp:
            exp = json.load(fp)
        gd = MockGameScore("tests/data/game_2018122314_gtd.json")
        got = gd.getGameScore(sch)
        self.assertEqual(got, exp)
    
    def test_getGameScore_dataframe(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122314_score.json", "rt") as fp:
            exp = pandas.DataFrame(json.load(fp))
        gd = MockGameScore("tests/data/game_2018122314_gtd.json")
        got = gd.getGameScore(sch, pandas.DataFrame)
        self.assertTrue(all(got.eq(exp)))
    
    def test_getGameScore_2nd_call_list(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        gd = MockGameScore("tests/data/game_2018122314_gtd.json")
        got = gd.getGameScore(sch)
        gsis_id = "2018122313"
        sch = self.getSchedule(gsis_id)
        gd.srcpath = "tests/data/game_2018122313_gtd.json"
        got = gd.getGameScore(sch)
        with open("tests/data/game_2018122313_score.json", "rt") as fp:
            exp = json.load(fp)
        self.assertEqual(got, exp)

class MockGameScore(MockGameData, GameScore):

    def __init__(self, srcpath : str):
        super(MockGameScore, self).__init__(srcpath)
