import unittest
import json
import pandas
from tests.MockGameData import MockGameData
from nflapi.GamePlay import GamePlay

class TestGamePlay(unittest.TestCase):
    def getSchedule(self, gsis_id : str) -> dict:
        with open("tests/data/schedule_2018_reg_16.json", "rt") as rfp:
            sch = json.load(rfp)
            il = [i for i in range(0, len(sch)) if sch[i]["gsis_id"] == gsis_id]
            return sch[il[0]]

    def test__doPlayerItemParse51(self):
        item = {
            "sequence": 3,
            "clubcode": "KC",
            "playerName": None,
            "statId": 51,
            "yards": 0.0
        }
        d = {"player_id": 0}
        gp = GamePlay()
        got = gp._doPlayerItemParse(item, d)
        exp = {
            "player_id": 0,
            "sequence": 3,
            "team": "KC",
            "player_abrv_name": None,
            "kickret_touchback": 1,
            "stat_id": 51,
            "stat_cat": "team",
            "stat_desc": "Kickoff - touchback",
            "stat_desc_long": "Kick resulted in a touchback. A touchback implies that "
                              "there is no return."
        }
        self.assertEqual(got, exp)

    def test__doPlayerItemParse410(self):
        item = {
            "sequence": 1,
            "clubcode": "SEA",
            "playerName": "S.Janikowski",
            "statId": 410,
            "yards": 75.0
        }
        d = {"player_id": 0}
        gp = GamePlay()
        got = gp._doPlayerItemParse(item, d)
        exp = {
            "player_id": 0,
            "sequence": 1,
            "team": "SEA",
            "player_abrv_name": "S.Janikowski",
            "kicking_all_yds": 75.0,
            "stat_id": 410,
            "stat_cat": "kicking",
            "stat_desc": "Kickoff and length of kick",
            "stat_desc_long": "Kickoff and length of kick. Includes end zone yards "
                              "for all kicks into the end zone, including kickoffs "
                              "ending in a touchback."
        }
        self.assertEqual(got, exp)

    def test__doPlayerItemParse44(self):
        item = {
            "sequence": 2,
            "clubcode": "SEA",
            "playerName": "S.Janikowski",
            "statId": 44,
            "yards": 65.0
        }
        d = {"player_id": 0}
        gp = GamePlay()
        got = gp._doPlayerItemParse(item, d)
        exp = {
            "player_id": 0,
            "sequence": 2,
            "team": "SEA",
            "player_abrv_name": "S.Janikowski",
            "kicking_yds": 65.0,
            "kicking_tot": 1,
            "kicking_touchback": 1,
            "stat_id": 44,
            "stat_cat": "kicking",
            "stat_desc": "Kickoff with touchback",
            "stat_desc_long": "Kickoff resulted in a touchback."
        }
        self.assertEqual(got, exp)

    def test__doPlayerParseKO(self):
        pldata = {
            "0": [
                {
                    "sequence": 3,
                    "clubcode": "KC",
                    "playerName": None,
                    "statId": 51,
                    "yards": 0.0
                }
            ],
            "00-0019646": [
                {
                    "sequence": 1,
                    "clubcode": "SEA",
                    "playerName": "S.Janikowski",
                    "statId": 410,
                    "yards": 75.0
                },
                {
                    "sequence": 2,
                    "clubcode": "SEA",
                    "playerName": "S.Janikowski",
                    "statId": 44,
                    "yards": 65.0
                }
            ]
        }
        gp = GamePlay()
        got = gp._doPlayerParse(pldata, {})
        exp = [
            {"player_id": "0", "sequence": 3, "team": "KC",
             "player_abrv_name": None, "kickret_touchback": 1,
             "stat_id": 51, "stat_cat": "team", "stat_desc": "Kickoff - touchback",
             "stat_desc_long": "Kick resulted in a touchback. A touchback implies that "
                               "there is no return."},
            {"player_id": "00-0019646", "sequence": 1, "team": "SEA",
             "player_abrv_name": "S.Janikowski",
             "kicking_all_yds": 75.0, "stat_id": 410,
             "stat_cat": "kicking", "stat_desc": "Kickoff and length of kick",
             "stat_desc_long": "Kickoff and length of kick. Includes end zone yards "
                               "for all kicks into the end zone, including kickoffs "
                               "ending in a touchback."},
            {"player_id": "00-0019646", "sequence": 2, "team": "SEA",
             "player_abrv_name": "S.Janikowski",
             "kicking_yds": 65.0, "kicking_tot": 1,
             "kicking_touchback": 1, "stat_id": 44,
             "stat_cat": "kicking", "stat_desc": "Kickoff with touchback",
             "stat_desc_long": "Kickoff resulted in a touchback."}
        ]
        self.assertEqual(got, exp)
    
    def test_getGamePlay_list(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122314_play.json", "rt") as fp:
            exp = json.load(fp)
        gd = MockGamePlay("tests/data/game_2018122314_gtd.json")
        got = gd.getGamePlay(sch)
        self.assertEqual(got, exp)
    
    def test_getGamePlay_dataframe(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122314_play.json", "rt") as fp:
            exp = pandas.DataFrame(json.load(fp))
        gd = MockGamePlay("tests/data/game_2018122314_gtd.json")
        got = gd.getGamePlay(sch, pandas.DataFrame)
        self.assertTrue(all(got.eq(exp)))
    
    def test_getGamePlay_2nd_call(self):
        gsis_id = "2018122314"
        sch = self.getSchedule(gsis_id)
        with open("tests/data/game_2018122313_play.json", "rt") as fp:
            exp = json.load(fp)
        gd = MockGamePlay("tests/data/game_2018122314_gtd.json")
        got = gd.getGamePlay(sch)
        gsis_id = "2018122313"
        sch = self.getSchedule(gsis_id)
        gd.srcpath = "tests/data/game_2018122313_gtd.json"
        got = gd.getGamePlay(sch)
        self.assertEqual(got, exp)
    
class MockGamePlay(MockGameData, GamePlay):
    
    def __init__(self, srcpath : str):
        super(MockGamePlay, self).__init__(srcpath)
    