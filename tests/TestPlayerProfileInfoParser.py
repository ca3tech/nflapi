import unittest
from bs4 import BeautifulSoup
from nflapi.PlayerProfileInfoParser import PlayerProfileInfoParser

class TestPlayerProfileInfoParser(unittest.TestCase):
    def setUp(self):
        self.parser = PlayerProfileInfoParser()

    def test_parse(self):
        tag = '''
        <div id="player-info">
            <p>
			    <strong>Height</strong>: 6-3 &nbsp; 
				<strong>Weight</strong>: 230 &nbsp; 
				<strong>Age</strong>: 23
			</p>
			<p><strong>Born</strong>: 9/17/1995 Tyler , TX</p>
			<p><strong>College</strong>: Texas Tech</p>
			<p><strong>Experience</strong>: 3rd season </p>
			<p><strong>High School</strong>: Whitehouse HS [TX]</p>
        </div>
        '''
        exp = [{
            "height": "6-3",
            "weight": 230,
            "age": 23,
            "born": "9/17/1995 Tyler, TX",
            "college": "Texas Tech",
            "experience": "3rd season",
            "high_school": "Whitehouse HS [TX]"
        }]
        bs = BeautifulSoup(tag, "html.parser")
        self.assertEqual(self.parser.parse(bs.div), exp)

if __name__ == "__main__":
    unittest.main()




