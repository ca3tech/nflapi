import unittest
import os
import re
import json
import pandas
import time
from nflapi.CachedAPI import ListOrDataFrame
from nflapi.Schedule import Schedule

class TestSchedule(unittest.TestCase):
    """ Test the Schedule class """

    def test_getSchedule_one_week_list(self):
        obj = MockSchedule("tests/data/schedule_2018_reg_16.xml")
        schd = obj.getSchedule(2018, "regular_season", 16)
        xschd = getExpectedResults("tests/data/schedule_2018_reg_16.json")
        self.assertEqual(schd, xschd)

    def test_getSchedule_one_week_dataframe(self):
        obj = MockSchedule("tests/data/schedule_2018_reg_16.xml")
        schdf = obj.getSchedule(2018, "regular_season", 16, pandas.DataFrame)
        xschdf = getExpectedResults("tests/data/schedule_2018_reg_16.json", pandas.DataFrame)
        self.assertEqual(len(schdf), len(xschdf), "row count differs")
        self.assertTrue(all(schdf.eq(xschdf, axis="columns")), "data does not match")

    @unittest.skip("unset to run test that actually hits the nfl api")
    def test_getSchedule_one_week_list_live(self):
        obj = Schedule()
        schd = obj.getSchedule(2018, "regular_season", 16)
        xschd = getExpectedResults("tests/data/schedule_2018_reg_16.json")
        self.assertEqual(schd, xschd)

    def test_getSchedule_two_week_2calls_list(self):
        obj = MockSchedule("tests/data/schedule_2018_reg_15.xml")
        schd = obj.getSchedule(2018, "regular_season", 15)
        obj.xmlpath = "tests/data/schedule_2018_reg_16.xml"
        schd = obj.getSchedule(2018, "regular_season", 16)
        self.assertEqual(obj.queryAPI_count, 2, "queryAPI call count unexpected")
        xschd = getExpectedResults("tests/data/schedule_2018_reg_16.json")
        self.assertEqual(schd, xschd)

    def test_getSchedule_one_week_2calls_cached_list(self):
        obj = MockSchedule("tests/data/schedule_2018_reg_16.xml")
        schd = obj.getSchedule(2018, "regular_season", 16)
        schd = obj.getSchedule(2018, "regular_season", 16)
        self.assertEqual(obj.queryAPI_count, 1, "queryAPI call count unexpected")
        xschd = getExpectedResults("tests/data/schedule_2018_reg_16.json")
        self.assertEqual(schd, xschd)

    def test_getSchedule_one_week_2calls_cached_dataframe(self):
        obj = MockSchedule("tests/data/schedule_2018_reg_16.xml")
        schdf = obj.getSchedule(2018, "regular_season", 16, pandas.DataFrame)
        schdf = obj.getSchedule(2018, "regular_season", 16, pandas.DataFrame)
        self.assertEqual(obj.queryAPI_count, 1, "queryAPI call count unexpected")
        xschdf = getExpectedResults("tests/data/schedule_2018_reg_16.json", pandas.DataFrame)
        self.assertTrue(all(schdf.eq(xschdf, axis="columns")), "data does not match")

    def test_getSchedule_two_week_2calls_cached_list(self):
        obj = MockSchedule("tests/data/schedule_2018_reg_16.xml")
        schd = obj.getSchedule(2018, "regular_season", 16)
        obj.xmlpath = "tests/data/schedule_2018_reg_15.xml"
        schd = obj.getSchedule(2018, "regular_season", 15)
        schd = obj.getSchedule(2018, "regular_season", 16)
        self.assertEqual(obj.queryAPI_count, 2, "queryAPI call count unexpected")
        xschd = getExpectedResults("tests/data/schedule_2018_reg_16.json")
        self.assertEqual(schd, xschd)

    def test_getSchedule_two_week_2calls_cached_dataframe(self):
        obj = MockSchedule("tests/data/schedule_2018_reg_16.xml")
        schdf = obj.getSchedule(2018, "regular_season", 16, pandas.DataFrame)
        obj.xmlpath = "tests/data/schedule_2018_reg_15.xml"
        schdf = obj.getSchedule(2018, "regular_season", 15, pandas.DataFrame)
        schdf = obj.getSchedule(2018, "regular_season", 16, pandas.DataFrame)
        self.assertEqual(obj.queryAPI_count, 2, "queryAPI call count unexpected")
        xschdf = getExpectedResults("tests/data/schedule_2018_reg_16.json", pandas.DataFrame)
        self.assertTrue(all(schdf.eq(xschdf, axis="columns")), "data does not match")

def getExpectedResults(jspath : str, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
    with open(jspath, "rt") as jfh:
        xschd = json.load(jfh)
        for i in range(0, len(xschd)):
            xschd[i]["date"] = time.strptime(xschd[i]["date"], "%Y-%m-%d %H:%M %z")
            xschd[i]["start_time"] = time.strptime(xschd[i]["start_time"], "%H:%M %z")
    if issubclass(return_type, pandas.DataFrame):
        xschd = pandas.DataFrame(xschd)
    return xschd

class MockSchedule(Schedule):
    def __init__(self, xmlpath : str):
        super(MockSchedule, self).__init__()
        self.xmlpath = xmlpath
        self._qapi_count = 0

    @property
    def queryAPI_count(self):
        return self._qapi_count

    @property
    def xmlpath(self) -> str:
        return self._xmlpath

    @xmlpath.setter
    def xmlpath(self, newpath):
        self._xmlpath = newpath
        with open(newpath, "rt") as fh:
            self._xmlstr = "".join(fh.readlines())

    def _queryAPI(self, query_doc : dict) -> str:
        self._qapi_count += 1
        self._queryDoc = query_doc
        return self._xmlstr

    @property
    def _queryDoc(self) -> dict:
        return self._query_doc

    @_queryDoc.setter
    def _queryDoc(self, doc : dict):
        self._query_doc = doc

if __name__ == "__main__":
    unittest.main()
