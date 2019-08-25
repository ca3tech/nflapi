import unittest
import os
import time
import xml.sax
import json
from nflapi.ScheduleContentHandler import ScheduleContentHandler

class TestScheduleContentHandler(unittest.TestCase):
    """ Test the ScheduleContentHandler class """

    def setUp(self):
        self.handler = ScheduleContentHandler()

    def test_startElement_gms_reg(self):
        self.handler.startElement("gms", {"gd": "0", "w": "16", "y": "2018", "t": "R"})
        self.assertEqual(self.handler.season, 2018)
        self.assertEqual(self.handler.week, 16)
        self.assertEqual(self.handler.season_type, "regular_season")
        self.assertEqual(len(self.handler.list), 0, "game data is not empty")
        self.assertEqual(len(self.handler.dataframe), 0, "game dataframe is not empty")

    def test_startElement_gms_pre(self):
        self.handler.startElement("gms", {"gd": "0", "w": "1", "y": "2018", "t": "P"})
        self.assertEqual(self.handler.season, 2018)
        self.assertEqual(self.handler.week, 1)
        self.assertIsNone(self.handler.season_type)
        self.assertEqual(len(self.handler.list), 0, "game data is not empty")
        self.assertEqual(len(self.handler.dataframe), 0, "game dataframe is not empty")

    def test_startElement_g_reg_list(self):
        self.handler.startElement("gms", {"gd": "0", "w": "16", "y": "2018", "t": "R"})
        gd = {"eid": "2018122200", "gsis": "57794", "d": "Sat", "t": "4:30", "q": "F",
              "k": "", "h": "TEN", "hnn": "titans", "hs": "25", "v": "WAS",
              "vnn": "redskins", "vs": "16", "p": "", "rz": "", "ga": "", "gt": "REG"}
        self.handler.startElement("g", gd)
        self.assertEqual(self.handler.season, 2018)
        self.assertEqual(self.handler.week, 16)
        self.assertEqual(self.handler.season_type, "regular_season")
        d = self.handler.list
        self.assertIsNotNone(d)
        self.assertEqual(len(d), 1, "list does not have 1 record")
        self.assertEqual(d[0]["gsis_id"], gd["eid"], "gsis_id not expected")
        self.assertEqual(d[0]["gamekey"], gd["gsis"], "gamekey not expected")
        self.assertEqual(d[0]["day_of_week"], gd["d"], "day_of_week not expected")
        self.assertEqual(d[0]["start_time"], time.strptime("%s PM -0500" % gd["t"], "%I:%M %p %z"), "start_time not expected")
        self.assertEqual(d[0]["quarter"], gd["q"], "quarter not expected")
        self.assertEqual(d[0]["home_team"], gd["h"], "home_team not expected")
        self.assertEqual(d[0]["home_team_name"], gd["hnn"], "home_team_name not expected")
        self.assertEqual(d[0]["home_team_score"], int(gd["hs"]), "home_team_score not expected")
        self.assertEqual(d[0]["away_team"], gd["v"], "away_team not expected")
        self.assertEqual(d[0]["away_team_name"], gd["vnn"], "away_team_name not expected")
        self.assertEqual(d[0]["away_team_score"], int(gd["vs"]), "away_team_score not expected")
        self.assertEqual(d[0]["finished"], True, "finished not expected")
        self.assertEqual(d[0]["season"], self.handler.season, "season not expected")
        self.assertEqual(d[0]["week"], self.handler.week, "week not expected")
        self.assertEqual(d[0]["season_type"], "regular_season", "season_type not expected")
        self.assertEqual(d[0]["date"], time.strptime("2018-12-22 16:30 -0500", "%Y-%m-%d %H:%M %z"), "date not expected")

    def test_startElement_g_reg_am_list(self):
        self.handler.startElement("gms", {"gd": "0", "w": "16", "y": "2018", "t": "R"})
        gd = {"eid": "2018122200", "gsis": "57794", "d": "Sat", "t": "9:00", "q": "F",
              "k": "", "h": "TEN", "hnn": "titans", "hs": "25", "v": "WAS",
              "vnn": "redskins", "vs": "16", "p": "", "rz": "", "ga": "", "gt": "REG"}
        self.handler.startElement("g", gd)
        self.assertEqual(self.handler.season, 2018)
        self.assertEqual(self.handler.week, 16)
        self.assertEqual(self.handler.season_type, "regular_season")
        d = self.handler.list
        self.assertIsNotNone(d)
        self.assertEqual(len(d), 1, "list does not have 1 record")
        self.assertEqual(d[0]["gsis_id"], gd["eid"], "gsis_id not expected")
        self.assertEqual(d[0]["gamekey"], gd["gsis"], "gamekey not expected")
        self.assertEqual(d[0]["day_of_week"], gd["d"], "day_of_week not expected")
        self.assertEqual(d[0]["start_time"], time.strptime("%s AM -0500" % gd["t"], "%I:%M %p %z"), "start_time not expected")
        self.assertEqual(d[0]["quarter"], gd["q"], "quarter not expected")
        self.assertEqual(d[0]["home_team"], gd["h"], "home_team not expected")
        self.assertEqual(d[0]["home_team_name"], gd["hnn"], "home_team_name not expected")
        self.assertEqual(d[0]["home_team_score"], int(gd["hs"]), "home_team_score not expected")
        self.assertEqual(d[0]["away_team"], gd["v"], "away_team not expected")
        self.assertEqual(d[0]["away_team_name"], gd["vnn"], "away_team_name not expected")
        self.assertEqual(d[0]["away_team_score"], int(gd["vs"]), "away_team_score not expected")
        self.assertEqual(d[0]["finished"], True, "finished not expected")
        self.assertEqual(d[0]["season"], self.handler.season, "season not expected")
        self.assertEqual(d[0]["week"], self.handler.week, "week not expected")
        self.assertEqual(d[0]["season_type"], "regular_season", "season_type not expected")
        self.assertEqual(d[0]["date"], time.strptime("2018-12-22 09:00 -0500", "%Y-%m-%d %H:%M %z"), "date not expected")

    def test_startElement_g_reg_future_list(self):
        self.handler.startElement("gms", {"gd": "0", "w": "16", "y": "2018", "t": "R"})
        gd = {"eid": "2018122200", "gsis": "57794", "d": "Sat", "t": "4:30", "q": "P",
              "k": "", "h": "TEN", "hnn": "titans", "hs": "", "v": "WAS",
              "vnn": "redskins", "vs": "", "p": "", "rz": "", "ga": "", "gt": "REG"}
        self.handler.startElement("g", gd)
        self.assertEqual(self.handler.season, 2018)
        self.assertEqual(self.handler.week, 16)
        self.assertEqual(self.handler.season_type, "regular_season")
        d = self.handler.list
        self.assertIsNotNone(d)
        self.assertEqual(len(d), 1, "list does not have 1 record")
        self.assertEqual(d[0]["gsis_id"], gd["eid"], "gsis_id not expected")
        self.assertEqual(d[0]["gamekey"], gd["gsis"], "gamekey not expected")
        self.assertEqual(d[0]["day_of_week"], gd["d"], "day_of_week not expected")
        self.assertEqual(d[0]["start_time"], time.strptime("%s PM -0500" % gd["t"], "%I:%M %p %z"), "start_time not expected")
        self.assertEqual(d[0]["quarter"], gd["q"], "quarter not expected")
        self.assertEqual(d[0]["home_team"], gd["h"], "home_team not expected")
        self.assertEqual(d[0]["home_team_name"], gd["hnn"], "home_team_name not expected")
        self.assertEqual(d[0]["home_team_score"], None, "home_team_score not expected")
        self.assertEqual(d[0]["away_team"], gd["v"], "away_team not expected")
        self.assertEqual(d[0]["away_team_name"], gd["vnn"], "away_team_name not expected")
        self.assertEqual(d[0]["away_team_score"], None, "away_team_score not expected")
        self.assertEqual(d[0]["finished"], False, "finished not expected")
        self.assertEqual(d[0]["season"], self.handler.season, "season not expected")
        self.assertEqual(d[0]["week"], self.handler.week, "week not expected")
        self.assertEqual(d[0]["season_type"], "regular_season", "season_type not expected")
        self.assertEqual(d[0]["date"], time.strptime("2018-12-22 16:30 -0500", "%Y-%m-%d %H:%M %z"), "date not expected")

    def test_startElement_g_reg(self):
        self.handler.startElement("gms", {"gd": "0", "w": "16", "y": "2018", "t": "R"})
        gd = {"eid": "2018122200", "gsis": "57794", "d": "Sat", "t": "4:30", "q": "F",
              "k": "", "h": "TEN", "hnn": "titans", "hs": "25", "v": "WAS",
              "vnn": "redskins", "vs": "16", "p": "", "rz": "", "ga": "", "gt": "REG"}
        self.handler.startElement("g", gd)
        self.assertEqual(self.handler.season, 2018)
        self.assertEqual(self.handler.week, 16)
        self.assertEqual(self.handler.season_type, "regular_season")
        df = self.handler.dataframe
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 1, "dataframe does not have 1 row")
        self.assertEqual(df.gsis_id.to_list(), [gd["eid"]], "gsis_id not expected")
        self.assertEqual(df.gamekey.to_list(), [gd["gsis"]], "gamekey not expected")
        self.assertEqual(df.day_of_week.to_list(), [gd["d"]], "day_of_week not expected")
        self.assertEqual(df.start_time.to_list(), [time.strptime("%s PM -0500" % gd["t"], "%I:%M %p %z")], "start_time not expected")
        self.assertEqual(df.quarter.to_list(), [gd["q"]], "quarter not expected")
        self.assertEqual(df.home_team.to_list(), [gd["h"]], "home_team not expected")
        self.assertEqual(df.home_team_name.to_list(), [gd["hnn"]], "home_team_name not expected")
        self.assertEqual(df.home_team_score.to_list(), [int(gd["hs"])], "home_team_score not expected")
        self.assertEqual(df.away_team.to_list(), [gd["v"]], "away_team not expected")
        self.assertEqual(df.away_team_name.to_list(), [gd["vnn"]], "away_team_name not expected")
        self.assertEqual(df.away_team_score.to_list(), [int(gd["vs"])], "away_team_score not expected")
        self.assertEqual(df.finished.to_list(), [True], "finished not expected")
        self.assertEqual(df.season.to_list(), [self.handler.season], "season not expected")
        self.assertEqual(df.week.to_list(), [self.handler.week], "week not expected")
        self.assertEqual(df.season_type.to_list(), ["regular_season"], "season_type not expected")
        self.assertEqual(df.date.to_list(), [time.strptime("2018-12-22 16:30 -0500", "%Y-%m-%d %H:%M %z")], "date not expected")

    def test_startElement_g_reg_am(self):
        self.handler.startElement("gms", {"gd": "0", "w": "16", "y": "2018", "t": "R"})
        gd = {"eid": "2018122200", "gsis": "57794", "d": "Sat", "t": "9:00", "q": "F",
              "k": "", "h": "TEN", "hnn": "titans", "hs": "25", "v": "WAS",
              "vnn": "redskins", "vs": "16", "p": "", "rz": "", "ga": "", "gt": "REG"}
        self.handler.startElement("g", gd)
        self.assertEqual(self.handler.season, 2018)
        self.assertEqual(self.handler.week, 16)
        self.assertEqual(self.handler.season_type, "regular_season")
        df = self.handler.dataframe
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 1, "dataframe does not have 1 row")
        self.assertEqual(df.gsis_id.to_list(), [gd["eid"]], "gsis_id not expected")
        self.assertEqual(df.gamekey.to_list(), [gd["gsis"]], "gamekey not expected")
        self.assertEqual(df.day_of_week.to_list(), [gd["d"]], "day_of_week not expected")
        self.assertEqual(df.start_time.to_list(), [time.strptime("%s AM -0500" % gd["t"], "%I:%M %p %z")], "start_time not expected")
        self.assertEqual(df.quarter.to_list(), [gd["q"]], "quarter not expected")
        self.assertEqual(df.home_team.to_list(), [gd["h"]], "home_team not expected")
        self.assertEqual(df.home_team_name.to_list(), [gd["hnn"]], "home_team_name not expected")
        self.assertEqual(df.home_team_score.to_list(), [int(gd["hs"])], "home_team_score not expected")
        self.assertEqual(df.away_team.to_list(), [gd["v"]], "away_team not expected")
        self.assertEqual(df.away_team_name.to_list(), [gd["vnn"]], "away_team_name not expected")
        self.assertEqual(df.away_team_score.to_list(), [int(gd["vs"])], "away_team_score not expected")
        self.assertEqual(df.finished.to_list(), [True], "finished not expected")
        self.assertEqual(df.season.to_list(), [self.handler.season], "season not expected")
        self.assertEqual(df.week.to_list(), [self.handler.week], "week not expected")
        self.assertEqual(df.season_type.to_list(), ["regular_season"], "season_type not expected")
        self.assertEqual(df.date.to_list(), [time.strptime("2018-12-22 09:00 -0500", "%Y-%m-%d %H:%M %z")], "date not expected")

    def test_parse_reg_xml(self):
        with open(os.path.join("tests", "data", "schedule_2018_reg_16.xml"), "rt") as xfh:
            xml.sax.parse(xfh, self.handler)
            self.assertEqual(self.handler.season, 2018)
            self.assertEqual(self.handler.week, 16)
            self.assertEqual(self.handler.season_type, "regular_season")
            d = self.handler.list
            self.assertIsNotNone(d)
            self.assertEqual(len(d), 16, "dataframe does not have 1 row")
            self.assertEqual(d[0]["gsis_id"], "2018122200", "gsis_id not expected")
            self.assertEqual(d[0]["gamekey"], "57794", "gamekey not expected")
            self.assertEqual(d[0]["day_of_week"], "Sat", "day_of_week not expected")
            self.assertEqual(d[0]["start_time"], time.strptime("4:30 PM -0500", "%I:%M %p %z"), "start_time not expected")
            self.assertEqual(d[0]["quarter"], "F", "quarter not expected")
            self.assertEqual(d[0]["home_team"], "TEN", "home_team not expected")
            self.assertEqual(d[0]["home_team_name"], "titans", "home_team_name not expected")
            self.assertEqual(d[0]["home_team_score"], 25, "home_team_score not expected")
            self.assertEqual(d[0]["away_team"], "WAS", "away_team not expected")
            self.assertEqual(d[0]["away_team_name"], "redskins", "away_team_name not expected")
            self.assertEqual(d[0]["away_team_score"], 16, "away_team_score not expected")
            self.assertEqual(d[0]["finished"], True, "finished not expected")
            self.assertEqual(d[0]["season"], self.handler.season, "season not expected")
            self.assertEqual(d[0]["week"], self.handler.week, "week not expected")
            self.assertEqual(d[0]["season_type"], "regular_season", "season_type not expected")
            self.assertEqual(d[0]["date"], time.strptime("2018-12-22 16:30 -0500", "%Y-%m-%d %H:%M %z"), "date not expected")

            self.assertEqual(d[15]["gsis_id"], "2018122400", "gsis_id not expected")
            self.assertEqual(d[15]["gamekey"], "57806", "gamekey not expected")
            self.assertEqual(d[15]["day_of_week"], "Mon", "day_of_week not expected")
            self.assertEqual(d[15]["start_time"], time.strptime("8:15 PM -0500", "%I:%M %p %z"), "start_time not expected")
            self.assertEqual(d[15]["quarter"], "F", "quarter not expected")
            self.assertEqual(d[15]["home_team"], "OAK", "home_team not expected")
            self.assertEqual(d[15]["home_team_name"], "raiders", "home_team_name not expected")
            self.assertEqual(d[15]["home_team_score"], 27, "home_team_score not expected")
            self.assertEqual(d[15]["away_team"], "DEN", "away_team not expected")
            self.assertEqual(d[15]["away_team_name"], "broncos", "away_team_name not expected")
            self.assertEqual(d[15]["away_team_score"], 14, "away_team_score not expected")
            self.assertEqual(d[15]["finished"], True, "finished not expected")
            self.assertEqual(d[15]["season"], self.handler.season, "season not expected")
            self.assertEqual(d[15]["week"], self.handler.week, "week not expected")
            self.assertEqual(d[15]["season_type"], "regular_season", "season_type not expected")
            self.assertEqual(d[15]["date"], time.strptime("2018-12-24 20:15 -0500", "%Y-%m-%d %H:%M %z"), "date not expected")

if __name__ == "__main__":
    unittest.main()
