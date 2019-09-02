import unittest
import nflapi.Utilities as util

class TestUtilities(unittest.TestCase):

    def test_parseYardLine_opp(self):
        self.assertEqual(util.parseYardLine("opp 30", "self"), 20)
    
    def test_parseYardLine_self(self):
        self.assertEqual(util.parseYardLine("self 30", "self"), -20)

    def test_parseYardLine_50(self):
        self.assertEqual(util.parseYardLine("50", "self"), 0)
