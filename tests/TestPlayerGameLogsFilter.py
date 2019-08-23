import unittest
from bs4 import BeautifulSoup
from nflapi.PlayerGameLogsFilter import PlayerGameLogsFilter

class TestPlayerGameLogsFilter(unittest.TestCase):
    def setUp(self):
        self.filter = PlayerGameLogsFilter()

    def test_filter_true_for_gl_tag(self):
        bs = BeautifulSoup('<table  class="data-table1" width="100%" border="0" summary="Game Logs For Patrick Mahomes In 2018"></table>', "html.parser")
        self.assertTrue(self.filter.match(bs.table))

    def test_filter_false_for_classless_table_tag(self):
        bs = BeautifulSoup('<table></table>', "html.parser")
        self.assertFalse(self.filter.match(bs.table))

    def test_filter_false_for_summaryless_table_tag(self):
        bs = BeautifulSoup('<table class="data-table1"></table>', "html.parser")
        self.assertFalse(self.filter.match(bs.table))

    def test_filter_false_for_nongl_table_tag(self):
        bs = BeautifulSoup('<table class="somethingelse"></table>', "html.parser")
        self.assertFalse(self.filter.match(bs.table))

    def test_filter_false_for_nongl_summary_table_tag(self):
        bs = BeautifulSoup('<table  class="data-table1" width="100%" border="0" summary="Some Other Data"></table>', "html.parser")
        self.assertFalse(self.filter.match(bs.table))

    def test_filter_false_for_nontable_tag(self):
        bs = BeautifulSoup('<a href="http://my.awesome.website">here</a>', "html.parser")
        self.assertFalse(self.filter.match(bs.a))

if __name__ == "__main__":
    unittest.main()
