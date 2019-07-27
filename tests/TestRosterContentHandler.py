import unittest
import pandas
from io import StringIO
import xml.sax
from bs4 import BeautifulSoup
import json
from nflapi.RosterContentHandler import RosterContentHandler

class TestRosterContentHandler(unittest.TestCase):
    """ Test the RosterContentHandler class """

    def setUp(self):
        self.domain = "http://my.test.com"
        self.handler = RosterContentHandler(self.domain)

    def test_startElement_table_tag_list(self):
        self.handler.startElement("table", {})
        self.assertEqual(self.handler.list, [])

    def test_startElement_nonteam_meta_tag_list(self):
        self.handler.startElement("meta", {"id": "someid", "other": "attribute"})
        self.assertEqual(self.handler.list, [])

    def test_startElement_team_meta_tag_list(self):
        self.handler.startElement("meta", {"id": "teamName", "content": "KC"})
        self.assertEqual(self.handler.list, [])
        self.assertEqual(self.handler._team, "KC", "_team attribute not set")

    def test_startElement_nonprofile_a_tag_list(self):
        self.handler.startElement("a", {"href": "http://my.awesome.com/website"})
        self.assertEqual(self.handler.list, [])

    def test_startElement_profile_a_tag(self):
        pid = 2558125
        pname = "patrickmahomes"
        purl = f"/player/{pname}/{pid}/profile"
        self.handler.startElement("a", {"href": purl})
        self.assertEqual(self.handler._processing_profile,
                         {"profile_id": pid,
                          "profile_name": "patrickmahomes",
                          "profile_url": f"{self.domain}{purl}"})

    def test_startElement_profile_a_tag_after_team(self):
        pid = 2558125
        pname = "patrickmahomes"
        purl = f"/player/{pname}/{pid}/profile"
        self.handler.startElement("meta", {"id": "teamName", "content": "KC"})
        self.handler.startElement("a", {"href": purl})
        self.assertEqual(self.handler._processing_profile,
                         {"profile_id": pid,
                          "profile_name": "patrickmahomes",
                          "profile_url": f"{self.domain}{purl}",
                           "team": "KC"})

    def test_startElement_profile_a_tag_then_characters(self):
        pid = 2558125
        pname = "patrickmahomes"
        purl = f"/player/{pname}/{pid}/profile"
        lname = "Mahomes"
        fname = "Patrick"
        pname = f"{lname}, {fname}"
        self.handler.startElement("a", {"href": purl})
        self.handler.characters(pname)
        self.assertEqual(self.handler._processing_profile,
                         {"profile_id": pid,
                          "profile_name": "patrickmahomes",
                          "profile_url": f"{self.domain}{purl}",
                           "first_name": fname,
                           "last_name": lname})

    def test_startElement_profile_a_tag_then_characters_then_endElement_list(self):
        pid = 2558125
        pname = "patrickmahomes"
        purl = f"/player/{pname}/{pid}/profile"
        lname = "Mahomes"
        fname = "Patrick"
        pname = f"{lname}, {fname}"
        self.handler.startElement("a", {"href": purl})
        self.handler.characters(pname)
        self.handler.endElement("a")
        self.assertEqual(self.handler.list,
                         [{"profile_id": pid,
                           "profile_name": "patrickmahomes",
                           "profile_url": f"{self.domain}{purl}",
                           "first_name": fname,
                           "last_name": lname}])

    def test_startElement_profile_a_tag_then_characters_then_endElement_with_team_list(self):
        pid = 2558125
        pname = "patrickmahomes"
        purl = f"/player/{pname}/{pid}/profile"
        lname = "Mahomes"
        fname = "Patrick"
        pname = f"{lname}, {fname}"
        self.handler.startElement("meta", {"id": "teamName", "content": "KC"})
        self.handler.startElement("a", {"href": purl})
        self.handler.characters(pname)
        self.handler.endElement("a")
        self.assertEqual(self.handler.list,
                         [{"profile_id": pid,
                           "profile_name": "patrickmahomes",
                           "profile_url": f"{self.domain}{purl}",
                           "team": "KC",
                           "first_name": fname,
                           "last_name": lname}])

    def test_startElement_profile_a_tag_then_characters_then_endElement_with_team_dataframe(self):
        pid = 2558125
        pname = "patrickmahomes"
        purl = f"/player/{pname}/{pid}/profile"
        lname = "Mahomes"
        fname = "Patrick"
        pname = f"{lname}, {fname}"
        self.handler.startElement("meta", {"id": "teamName", "content": "KC"})
        self.handler.startElement("a", {"href": purl})
        self.handler.characters(pname)
        self.handler.endElement("a")
        xdf = pandas.DataFrame([{"profile_id": pid,
                                            "profile_name": "patrickmahomes",
                                            "profile_url": f"{self.domain}{purl}",
                                            "team": "KC",
                                            "first_name": fname,
                                            "last_name": lname}])
        self.assertTrue(all(self.handler.dataframe.eq(xdf, axis="columns")))

    def test_document_processing(self):
        with StringIO() as doc:
            doc.write("<data>")
            with open("tests/data/roster_kc.html") as fp:
                soup = BeautifulSoup(fp)
                for tag in soup.find_all(["meta", "a"]):
                    doc.write(str(tag))
                doc.write("</data>")
            with open("tests/data/roster_kc.xml", "wt") as ofp:
                ofp.write(doc.getvalue())
            xml.sax.parseString(doc.getvalue(), self.handler)
        data = self.handler.list
        with open("tests/data/roster_kc.json", "rt") as fp:
            xdata = json.load(fp)
            self.assertEqual(data, xdata)
