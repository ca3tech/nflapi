import unittest
from bs4 import BeautifulSoup
from nflapi.PlayerProfileBioFilter import PlayerProfileBioFilter

class TestPlayerProfileBioFilter(unittest.TestCase):
    def setUp(self):
        self.filter = PlayerProfileBioFilter()

    def test_filter_true_for_bio_tag(self):
        bs = BeautifulSoup('<div id="player-bio"></div>', "html.parser")
        self.assertTrue(self.filter.match(bs.div))

    def test_filter_false_for_idless_div_tag(self):
        bs = BeautifulSoup('<div></div>', "html.parser")
        self.assertFalse(self.filter.match(bs.div))

    def test_filter_false_for_nonbio_div_tag(self):
        bs = BeautifulSoup('<div id="somethingelse"></div>', "html.parser")
        self.assertFalse(self.filter.match(bs.div))

    def test_filter_false_for_nondiv_tag(self):
        bs = BeautifulSoup('<a href="http://my.awesume.website">here</a>', "html.parser")
        self.assertFalse(self.filter.match(bs.a))

if __name__ == "__main__":
    unittest.main()
