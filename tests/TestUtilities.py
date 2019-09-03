import unittest
import nflapi.Utilities as util

class TestUtilities(unittest.TestCase):

    def test_parseYardLine_opp(self):
        self.assertEqual(util.parseYardLine("opp 30", "self"), 20)
    
    def test_parseYardLine_self(self):
        self.assertEqual(util.parseYardLine("self 30", "self"), -20)

    def test_parseYardLine_50(self):
        self.assertEqual(util.parseYardLine("50", "self"), 0)

    def test_getStatMetadata_3(self):
        exp = {
            "stat_id": 3,
            'stat_cat': 'team',
            'stat_desc': '1st down (rushing)',
            'stat_desc_long': 'A first down or TD occurred due to a rush.'
        }
        self.assertEqual(util.getStatMetadata(3), exp)

    def test_getStatMetadata_5(self):
        exp = {
            "stat_id": 5,
            'stat_cat': 'team',
            'stat_desc': '1st down (penalty)',
            'stat_desc_long': 'A first down or TD occurred due to a penalty. A play can have a first down from a pass or rush and from a penalty.'
        }
        self.assertEqual(util.getStatMetadata(5), exp)
