import unittest
import json
import datetime
import time
from dateutil import relativedelta
from nflapi.Client import Client
from nflapi.Schedule import Schedule
from nflapi.PlayerProfile import PlayerProfile
import tests.TestSchedule as tsch
import tests.TestPlayerProfile as tpprof

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()

    def test__currentWeek(self):
        self.client._currentDate = datetime.date(2019, 8, 29)
        self.assertEqual(self.client._currentWeek, -1,
                         "fifth week of 2019 preseason")
        self.client._currentDate = datetime.date(2019, 8, 1)
        self.assertEqual(self.client._currentWeek, -5,
                         "first week of 2019 preseason")
        self.client._currentDate = datetime.date(2019, 7, 30)
        self.assertEqual(self.client._currentWeek, 22,
                         "after 2018 season / before 2019 season")
        # Test every regular and postseason week of 2019 season
        qdt = datetime.date(2019, 9, 3)
        for xwk in range(1, 23):
            self.client._currentDate = qdt
            self.assertEqual(self.client._currentWeek, xwk, f"{qdt} week")
            qdt = qdt + relativedelta.relativedelta(weeks=1)

    def test_getSchedule_sstw(self):
        self.client._schedule = tsch.MockSchedule("tests/data/schedule_2018_reg_16.xml")
        exp = tsch.getExpectedResults("tests/data/schedule_2018_reg_16.json", list)
        got = self.client.getSchedule(season=2018, season_type="regular_season", week=16)
        self.assertEqual(got, exp)

    def test_getSchedule_none(self):
        self.client._schedule = tsch.MockSchedule("tests/data/schedule_2018_reg_15.xml")
        self.client._currentDate = datetime.date(2018, 12, 11)
        exp = tsch.getExpectedResults("tests/data/schedule_2018_reg_15.json", list)
        got = self.client.getSchedule()
        self.assertEqual(self.client._currentSeason, 2018, "season mismatch")
        self.assertEqual(self.client._currentSeasonType, "regular_season", "season type mismatch")
        self.assertEqual(self.client._currentWeek, 15, "week mismatch")
        self.assertEqual(self.client._schedule._queryDoc,
                         {"season": 2018, "seasonType": "REG", "week": 15},
                         "schedule query not expected")
        self.assertEqual(got, exp)

    def test_getSchedule_s(self):
        self.client._schedule = Schedule()
        got = self.client.getSchedule(season=2018)
        tstmap = {
            "preseason": lambda s: min(s) == 0 and max(s) == 4,
            "regular_season": lambda s: min(s) == 1 and max(s) == 17,
            "postseason": lambda s: min(s) == 18 and max(s) == 22
        }
        wkmap = {"preseason": set(), "regular_season": set(), "postseason": set()}
        for d in got:
            wkmap[d["season_type"]].add(d["week"])
        for st, tester in tstmap.items():
            self.assertTrue(tester(wkmap[st]), f"{st} test failed")

    def test_getSchedule_sstpre(self):
        self.client._schedule = Schedule()
        got = self.client.getSchedule(season=2018, season_type="preseason")
        tstmap = {
            "preseason": lambda s: min(s) == 0 and max(s) == 4,
            "regular_season": lambda s: len(s) == 0,
            "postseason": lambda s: len(s) == 0
        }
        wkmap = {"preseason": set(), "regular_season": set(), "postseason": set()}
        for d in got:
            wkmap[d["season_type"]].add(d["week"])
        for st, tester in tstmap.items():
            self.assertTrue(tester(wkmap[st]), f"{st} test failed")

    def test_getSchedule_sstreg(self):
        self.client._schedule = Schedule()
        got = self.client.getSchedule(season=2018, season_type="regular_season")
        tstmap = {
            "preseason": lambda s: len(s) == 0,
            "regular_season": lambda s: min(s) == 1 and max(s) == 17,
            "postseason": lambda s: len(s) == 0
        }
        wkmap = {"preseason": set(), "regular_season": set(), "postseason": set()}
        for d in got:
            wkmap[d["season_type"]].add(d["week"])
        for st, tester in tstmap.items():
            self.assertTrue(tester(wkmap[st]), f"{st} test failed")

    def test_getSchedule_sstpost(self):
        self.client._schedule = Schedule()
        got = self.client.getSchedule(season=2018, season_type="postseason")
        tstmap = {
            "preseason": lambda s: len(s) == 0,
            "regular_season": lambda s: len(s) == 0,
            "postseason": lambda s: min(s) == 18 and max(s) == 22
        }
        wkmap = {"preseason": set(), "regular_season": set(), "postseason": set()}
        for d in got:
            wkmap[d["season_type"]].add(d["week"])
        for st, tester in tstmap.items():
            self.assertTrue(tester(wkmap[st]), f"{st} test failed")

    def test_getPlayerProfile_invalid(self):
        self.client._playerProfile = tpprof.MockPlayerProfile("tests/data/invalid_profile.html")
        with open("tests/data/roster_kc.json", "rt") as fp:
            rosters = [r for r in json.load(fp) if r["profile_name"] == "nickallegretti"]
        self.assertEqual(self.client.getPlayerProfile(rosters, list), [])

class MockClient(Client):

    def __init__(self):
        super(MockClient, self).__init__()
        self._schedule = None
        self._curdt = None
        self._playerProfile = None

    @property
    def _schedule(self) -> tsch.Schedule:
        return self._schedule_v

    @_schedule.setter
    def _schedule(self, nschedule : tsch.Schedule):
        self._schedule_v = nschedule

    @property
    def _playerProfile(self) -> PlayerProfile:
        return self._plprof

    @_playerProfile.setter
    def _playerProfile(self, npprof : PlayerProfile):
        self._plprof = npprof

    @property
    def _currentDate(self) -> datetime.date:
        if self._curdt is None:
            self._currentDate = datetime.date.today()
        return self._curdt

    @_currentDate.setter
    def _currentDate(self, ncurdt : datetime.date):
        self._curdt = ncurdt
    