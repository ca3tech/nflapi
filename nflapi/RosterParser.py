from bs4 import Tag
import re
from datetime import datetime
import dateutil.parser
from typing import List
from nflapi.BSTagParser import BSTagParser

class RosterParser(BSTagParser):

    def __init__(self, domain : str, team : str = None):
        self._domain = domain
        self._team = team
        self._hdrs = []

    @property
    def team(self) -> str:
        return self._team

    @team.setter
    def team(self, newteam : str):
        self._team = newteam
    
    def parse(self, tag : Tag) -> List[dict]:
        """Parse a roster table
        
        Parameters
        ----------
        tag : Tag
            The table tag from BeautifulSoup
        
        Returns
        -------
        list of dict
            Each item corresponds to a data row
        """

        # First we need to parse the headers
        self._parseHeader(tag.find("tr"))
        # Now that we know what our columns are, parse the data
        tbtag = tag.find("tbody")
        data = []
        # For each row
        for trtag in tbtag.find_all("tr"):
            # Parse this data row into a list
            rl = self._parseBodyRow(trtag)
            if rl is not None:
                # Create a dict from the headers we determined
                # above and the data list we just created
                d = dict(zip(self._headers, rl))
                d = {}
                for i in range(0, len(rl)):
                    cvalue = rl[i]
                    if isinstance(cvalue, dict):
                        d.update(cvalue)
                    else:
                        d[self._headers[i]] = rl[i]
                d["team"] = self._team
                data.append(d)
        return data

    @property
    def _headers(self) -> list:
        return self._hdrs

    def _parseHeaderName(self, tdtag) -> str:
        nmap = {
            "no": "number",
            "pos": "position"
        }
        txt = self._getTagText(tdtag).lower()
        if txt in nmap:
            txt = nmap[txt]
        return txt

    def _parseHeader(self, trtag : Tag):
        tds : list = trtag.find_all("th")
        for td in tds:
            self._hdrs.append(self._parseHeaderName(td))

    def _parseBodyRow(self, trtag : Tag) -> list:
        tdtags = trtag.find_all("td")
        data = []
        for i in range(0, len(tdtags)):
            # Determine which function to pass the tag to
            # for extracting the value.
            pfun = self._getBodyColParser(self._headers[i])
            # Extract the value from the tag and add it to data
            data.append(pfun(tdtags[i]))
        return data

    def _getTagText(self, tag : Tag, underscores : bool = True, tolower : bool = True) -> str:
        txt = tag.get_text()
        # Get rid of trailing whitespace
        txt = re.sub(r"\s+$", "", txt)
        # Get rid of preceding whitespace
        txt = re.sub(r"^\s+", "", txt)
        # Change multiple consecutive whitespace characters
        # to a single space.
        txt = re.sub(r"\s{2,}", " ", txt)
        if underscores:
            # Change spaces to underscores
            txt = re.sub(" ", "_", txt)
        if tolower:
            # Convert the text to lower case
            txt = txt.lower()
        return txt

    def _getBodyColParser(self, header : str) -> callable:
        switch = {
            "number": self._int_parser,
            "weight": self._int_parser,
            "exp": self._int_parser,
            "birthdate": self._birthday_parser,
            "name": self._name_parser,
            "default": self._str_parser
        }
        if header in switch.keys():
            f = switch[header]
        else:
            f = switch["default"]
        return f

    def _name_parser(self, tdtag : Tag) -> dict:
        d = {}
        # The link tag contains the data we are interested in.
        atag = tdtag.find("a")
        pname = self._getTagText(atag, underscores=False, tolower=False)
        m = re.search(r"^([^\,]+)\,\s*(.+)$", pname)
        if m is not None:
            d["last_name"] = m.group(1)
            d["first_name"] = m.group(2)
        m = re.search(r"player/([^/]+)/(\d+)/profile", atag.attrs["href"])
        if m is not None:
            # Prefix the domain to the URL as it is relative
            purl = "{}{}".format(self._domain, atag.attrs["href"])
            csurl = purl.replace("profile", "careerstats")
            gsurl = purl.replace("profile", "gamesplits")
            glurl = purl.replace("profile", "gamelogs")
            d["profile_id"] = int(m.group(2))
            d["profile_name"] = m.group(1)
            d["profile_url"] = purl
            d["careerstats_url"] = csurl
            d["gamelogs_url"] = glurl
            d["gamesplits_url"] = gsurl
        return d

    def _str_parser(self, tdtag : Tag) -> str:
        v : str = self._getTagText(tdtag, underscores=False, tolower=False)
        if v in ["--", ""]:
            # The table uses -- and empty text to indicate
            # no data so set the value to None.
            v = None
        return v

    def _int_parser(self, tdtag : Tag) -> int:
        v = self._str_parser(tdtag)
        if v is not None:
            # Sometimes the integer has a T appended to it,
            # so we need to remove that before converting.
            v = int(re.sub(r"T$", "", v))
        return v

    def _birthday_parser(self, tdtag : Tag) -> datetime:
        v = self._str_parser(tdtag)
        if v is not None:
            try:
                v = dateutil.parser.parse(v, dayfirst=False)
            except ValueError:
                v = None
        return v
