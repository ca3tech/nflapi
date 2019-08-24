import unittest
from bs4 import BeautifulSoup
import time
import json
import pandas
from nflapi.PlayerGameLogsContentHandler import PlayerGameLogsContentHandler

class TestPlayerGameLogsContentHandler(unittest.TestCase):
    def setUp(self):
        self.handler = PlayerGameLogsContentHandler(2018)
    
    def getExpectedList(self, fpath = "tests/data/gamelogs_patrick_mahomes_2018_parse.json"):
        with open(fpath, "rt") as fp:
            recs = json.load(fp)
        for i in range(0, len(recs)):
            recs[i]["game_date"] = time.struct_time(recs[i]["game_date"])
        return recs

    def test_parse_list(self):
        with open("tests/data/gamelogs_patrick_mahomes_2018.html", "rt") as fp:
            doc = "".join(fp.readlines())
        self.handler.parse(doc)
        exp = self.getExpectedList()
        self.assertEqual(self.handler.list, exp)

    def test_parse_dataframe(self):
        with open("tests/data/gamelogs_patrick_mahomes_2018.html", "rt") as fp:
            doc = "".join(fp.readlines())
        self.handler.parse(doc)
        exp = pandas.DataFrame(self.getExpectedList())
        self.assertTrue(all(self.handler.dataframe.eq(exp, axis="columns")))

    def test_parse_rush_list(self):
        with open("tests/data/gamelogs_tyreek_hill_2018.html", "rt") as fp:
            doc = "".join(fp.readlines())
        self.handler.parse(doc)
        exp = self.getExpectedList("tests/data/gamelogs_tyreek_hill_2018_parse.json")
        self.assertEqual(self.handler.list, exp)

    def test_parse_kick_list(self):
        with open("tests/data/gamelogs_harrison_butker_2018.html", "rt") as fp:
            doc = "".join(fp.readlines())
        self.handler.parse(doc)
        exp = self.getExpectedList("tests/data/gamelogs_harrison_butker_2018_parse.json")
        self.assertEqual(self.handler.list, exp)

if __name__ == "__main__":
    unittest.main()




