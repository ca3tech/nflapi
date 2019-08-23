import unittest
from bs4 import BeautifulSoup
from nflapi.PlayerProfileInfoFilter import PlayerProfileInfoFilter

class TestPlayerProfileInfoFilter(unittest.TestCase):
    def setUp(self):
        self.filter = PlayerProfileInfoFilter()

    def test_filter_true_for_info_tag(self):
        bs = BeautifulSoup('<div class="player-info"></div>', "html.parser")
        self.assertTrue(self.filter.match(bs.div))

    def test_filter_false_for_classless_div_tag(self):
        bs = BeautifulSoup('<div></div>', "html.parser")
        self.assertFalse(self.filter.match(bs.div))

    def test_filter_false_for_noninfo_div_tag(self):
        bs = BeautifulSoup('<div class="somethingelse"></div>', "html.parser")
        self.assertFalse(self.filter.match(bs.div))

    def test_filter_false_for_nondiv_tag(self):
        bs = BeautifulSoup('<a href="http://my.awesome.website">here</a>', "html.parser")
        self.assertFalse(self.filter.match(bs.a))

if __name__ == "__main__":
    unittest.main()
