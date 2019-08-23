import unittest
from bs4 import BeautifulSoup
import time
import json
from nflapi.PlayerGameLogsParser import PlayerGameLogsParser

class TestPlayerGameLogsParser(unittest.TestCase):
    def setUp(self):
        self.parser = PlayerGameLogsParser(2018)

    def test__parseHeader(self):
        exp = ["wk", "game_date", "opp", "result",
               "games_g", "games_gs",
               "passing_comp", "passing_att", "passing_pct", "passing_yds", "passing_avg",
               "passing_td", "passing_int", "passing_sck", "passing_scky", "passing_rate",
               "rushing_att", "rushing_yds", "rushing_avg", "rushing_td",
               "fumbles_fum", "fumbles_lost"]
        with open("tests/data/gamelogs_patrick_mahomes_preseason_2018.html", "rt") as fp:
            bs = BeautifulSoup(fp, "html.parser")
        tag = bs.find("thead")
        self.parser._parseHeader(tag)
        self.assertEqual(self.parser._seasonType, "preseason", "_seasonType not expected")
        self.assertEqual(self.parser._headers, exp, "_headers not expected")

    def test__parseBodyRow(self):
        exp = [1, time.strptime("2018-08-09 -0500", "%Y-%m-%d %z"), "HOU", "10-17",
               1, 1,
               5, 7, 71.4, 33, 4.7, 0, 0, 1, 5, 81.2,
               None, None, None, None,
               None, None]
        with open("tests/data/gamelogs_patrick_mahomes_preseason_2018.html", "rt") as fp:
            bs = BeautifulSoup(fp, "html.parser")
        self.parser._parseHeader(bs.find("thead"))
        tbtag = bs.find("tbody")
        trtag = tbtag.find("tr")
        self.assertEqual(self.parser._parseBodyRow(trtag), exp, "data not expected")

    def test_parse(self):
        with open("tests/data/gamelogs_patrick_mahomes_preseason_2018_parse.json", "rt") as fp:
            exp = json.load(fp)
            for i in range(0, len(exp)):
                exp[i]["game_date"] = time.struct_time(exp[i]["game_date"])
        with open("tests/data/gamelogs_patrick_mahomes_preseason_2018.html", "rt") as fp:
            bs = BeautifulSoup(fp, "html.parser")
        data = self.parser.parse(bs)
        self.assertEqual(data, exp, "data not expected")


if __name__ == "__main__":
    unittest.main()




