import unittest
from bs4 import BeautifulSoup
import dateutil.parser
from nflapi.RosterParser import RosterParser

class TestRosterParser(unittest.TestCase):
    def setUp(self):
        self.domain = "http://my.test.com"
        self.team = "KC"
        self.parser = RosterParser(self.domain, self.team)

    def test_parse_one_rows(self):
        tag = '''
<table id="result" style="width:100%" cellpadding="0" class="data-table1" cellspacing="0">
<tr>
<th class="thd2 first sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=UNIFORM_NBR">No</a></th>
<th class="thd2 sortable sorted order1">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=1&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=PERSONS.LAST_NAME">Name</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=persons.primary_Position.id.position_Id">Pos</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=STATUS">Status</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=HEIGHT">Height</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=WEIGHT">Weight</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=BIRTH_DAY">Birthdate</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=NFL_EXPERIENCE">Exp</a></th>
<th class="thd2 last sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=persons.primary_College.COLLEGE_NAME">College</a></th></tr>
<tbody>
<tr class="odd">
<td>15</td>
<td style="text-align:left"> <a href="/player/patrickmahomes/2558125/profile">Mahomes, Patrick</a></td>
<td>QB</td>
<td>ACT</td>
<td> 6'3"</td>
<td>230</td>
<td>9/17/1995</td>
<td>3</td>
<td>Texas Tech</td></tr></tbody></table>
        '''
        pid = 2558125
        pname = "patrickmahomes"
        purl = f"{self.domain}/player/{pname}/{pid}/profile"
        csurl = f"{self.domain}/player/{pname}/{pid}/careerstats"
        gsurl = f"{self.domain}/player/{pname}/{pid}/gamesplits"
        glurl = f"{self.domain}/player/{pname}/{pid}/gamelogs"
        lname = "Mahomes"
        fname = "Patrick"
        exp = [{
            "number": 15,
            "last_name": lname,
            "first_name": fname,
            "profile_id": pid,
            "profile_name": "patrickmahomes",
            "profile_url": purl,
            "careerstats_url": csurl,
            "gamelogs_url": glurl,
            "gamesplits_url": gsurl,
            "position": "QB",
            "status": "ACT",
            "height": "6'3\"",
            "weight": 230,
            "birthdate": dateutil.parser.parse("9/17/1995", dayfirst=False),
            "exp": 3,
            "college": "Texas Tech",
            "team": self.team
        }]
        bs = BeautifulSoup(tag, "html.parser")
        self.assertEqual(self.parser.parse(bs.table), exp)

    def test_parse_two_row(self):
        tag = '''
<table id="result" style="width:100%" cellpadding="0" class="data-table1" cellspacing="0">
<tr>
<th class="thd2 first sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=UNIFORM_NBR">No</a></th>
<th class="thd2 sortable sorted order1">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=1&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=PERSONS.LAST_NAME">Name</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=persons.primary_Position.id.position_Id">Pos</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=STATUS">Status</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=HEIGHT">Height</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=WEIGHT">Weight</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=BIRTH_DAY">Birthdate</a></th>
<th class="thd2 sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=NFL_EXPERIENCE">Exp</a></th>
<th class="thd2 last sortable">
<a href="/teams/roster?d-447263-n=1&amp;d-447263-o=2&amp;team=KC&amp;d-447263-p=1&amp;d-447263-s=persons.primary_College.COLLEGE_NAME">College</a></th></tr>
<tbody>
<tr class="odd">
<td>15</td>
<td style="text-align:left"> <a href="/player/patrickmahomes/2558125/profile">Mahomes, Patrick</a></td>
<td>QB</td>
<td>ACT</td>
<td> 6'3"</td>
<td>230</td>
<td>9/17/1995</td>
<td>3</td>
<td>Texas Tech</td></tr>
<tr class="even">
<td>38</td>
<td style="text-align:left"> <a href="/player/marcusmarshall/2563152/profile">Marshall, Marcus</a></td>
<td>RB</td>
<td>ACT</td>
<td> 5'10"</td>
<td>200</td>
<td>//</td>
<td>0</td>
<td>James Madison</td></tr></tbody></table>
        '''
        pid = [2558125, 2563152]
        pname = ["patrickmahomes", "marcusmarshall"]
        purl = [f"{self.domain}/player/{pname[i]}/{pid[i]}/profile" for i in range(0, len(pname))]
        csurl = [f"{self.domain}/player/{pname[i]}/{pid[i]}/careerstats" for i in range(0, len(pname))]
        gsurl = [f"{self.domain}/player/{pname[i]}/{pid[i]}/gamesplits" for i in range(0, len(pname))]
        glurl = [f"{self.domain}/player/{pname[i]}/{pid[i]}/gamelogs" for i in range(0, len(pname))]
        lname = ["Mahomes", "Marshall"]
        fname = ["Patrick", "Marcus"]
        exp = [{
            "number": 15,
            "last_name": lname[0],
            "first_name": fname[0],
            "profile_id": pid[0],
            "profile_name": pname[0],
            "profile_url": purl[0],
            "careerstats_url": csurl[0],
            "gamelogs_url": glurl[0],
            "gamesplits_url": gsurl[0],
            "position": "QB",
            "status": "ACT",
            "height": "6'3\"",
            "weight": 230,
            "birthdate": dateutil.parser.parse("9/17/1995", dayfirst=False),
            "exp": 3,
            "college": "Texas Tech",
            "team": self.team
        }, {
            "number": 38,
            "last_name": lname[1],
            "first_name": fname[1],
            "profile_id": pid[1],
            "profile_name": pname[1],
            "profile_url": purl[1],
            "careerstats_url": csurl[1],
            "gamelogs_url": glurl[1],
            "gamesplits_url": gsurl[1],
            "position": "RB",
            "status": "ACT",
            "height": "5'10\"",
            "weight": 200,
            "birthdate": None,
            "exp": 0,
            "college": "James Madison",
            "team": self.team
        }]
        bs = BeautifulSoup(tag, "html.parser")
        self.assertEqual(self.parser.parse(bs.table), exp)