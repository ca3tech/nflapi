import unittest
import pandas
import json
import datetime
from nflapi.RosterContentHandler import RosterContentHandler
from nflapi.CachedAPI import ListOrDataFrame

class TestRosterContentHandler(unittest.TestCase):
    """ Test the RosterContentHandler class """

    def setUp(self):
        self.handler = RosterContentHandler("KC")

    def test_parse_list(self):
        with open("tests/data/roster_kc.html", "rt") as fp:
            self.handler.parse(fp.read())
            got = self.handler.list
        exp = getExpectedResults("tests/data/roster_kc.json", list)
        self.assertEqual(got, exp)

    def test_parse_dataframe(self):
        with open("tests/data/roster_kc.html", "rt") as fp:
            self.handler.parse(fp.read())
            got = self.handler.dataframe
        exp = getExpectedResults("tests/data/roster_kc.json", pandas.DataFrame)
        self.assertTrue(all(got.eq(exp)))

def getExpectedResults(jspath : str, return_type : ListOrDataFrame = list) -> ListOrDataFrame:
    with open(jspath, "rt") as jfh:
        xschd = json.load(jfh)
        for i in range(0, len(xschd)):
            if xschd[i]["birthdate"] is not None:
                xschd[i]["birthdate"] = datetime.datetime.strptime(xschd[i]["birthdate"], "%m/%d/%Y")
    if issubclass(return_type, pandas.DataFrame):
        xschd = pandas.DataFrame(xschd)
    return xschd

if __name__ == "__main__":
    unittest.main()
