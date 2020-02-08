import unittest
from bs4 import BeautifulSoup
import pandas
from nflapi.PlayerProfileContentHandler import PlayerProfileContentHandler

class TestPlayerProfileContentHandler(unittest.TestCase):
    def setUp(self):
        self.handler = PlayerProfileContentHandler()

    def test_parse_list(self):
        with open("tests/data/profile_patrick_mahomes.html", "rt") as fp:
            doc = "".join(fp.readlines())
        exp = [{
            "height": "6-3",
            "weight": 230,
            "age": 23,
            "born": "9/17/1995 Tyler, TX",
            "college": "Texas Tech",
            "experience": "3rd season",
            "high_school": "Whitehouse HS [TX]",
            "number": 15,
            "position": "QB"
        }]
        self.handler.parse(doc)
        self.assertEqual(self.handler.list, exp)

    def test_parse_dataframe(self):
        with open("tests/data/profile_patrick_mahomes.html", "rt") as fp:
            doc = "".join(fp.readlines())
        exp = pandas.DataFrame([{
            "height": "6-3",
            "weight": 230,
            "age": 23,
            "born": "9/17/1995 Tyler, TX",
            "college": "Texas Tech",
            "experience": "3rd season",
            "high_school": "Whitehouse HS [TX]",
            "number": 15,
            "position": "QB"
        }])
        self.handler.parse(doc)
        self.assertTrue(all(self.handler.dataframe.eq(exp, axis="columns")))

    def test_parse_invalid_list(self):
        with open("tests/data/invalid_profile.html", "rt") as fp:
            doc = "".join(fp.readlines())
        self.handler.parse(doc)
        self.assertEqual(self.handler.list, [])

if __name__ == "__main__":
    unittest.main()




