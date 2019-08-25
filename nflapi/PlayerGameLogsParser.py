from bs4 import Tag
import re
import time
from typing import List
from nflapi.BSTagParser import BSTagParser

class PlayerGameLogsParser(BSTagParser):

    def __init__(self, season : int):
        self._ssn = season
        self._ssntype = ""
        self._hdrs = []
    
    def parse(self, tag : Tag) -> List[dict]:
        """Parse a gamelogs table
        
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
        self._parseHeader(tag.find("thead"))
        # Now that we know what our columns are, parse the data
        tbtag = tag.find("tbody")
        data = []
        # For each row
        for trtag in tbtag.find_all("tr"):
            # Does this row contain content we care about?
            if self._incBodyRow(trtag):
                # Parse this data row into a list
                rl = self._parseBodyRow(trtag)
                if rl is not None:
                    # Create a dict from the headers we determined
                    # above and the data list we just created
                    d = dict(zip(self._headers, rl))
                    # Add the season that was passed in
                    d["season"] = self._season
                    # Add the season type which was determined
                    # when we parsed the headers
                    d["season_type"] = self._seasonType
                    data.append(d)
        return data

    @property
    def _season(self):
        return self._ssn

    @property
    def _seasonType(self) -> str:
        return self._ssntype

    @property
    def _headers(self) -> list:
        return self._hdrs

    def _parseHeader(self, thtag : Tag):
        # The header section of the table contains
        # 2 rows with the first being section names
        # and the second being the individual
        # column names. We want to append the second
        # row values to the first to form the full
        # header for the column.
        trs : list = thtag.find_all("tr")
        tds : list = trs[0].find_all("td")
        for i in range(0, len(tds)):
            tdtag = tds[i]
            if i == 0:
                # The first cell contains the season type and it
                # shouldn't be part of the header. Rather we want
                # to capture its value to be used later as the
                # season_type data column and we set its column
                # prefix to be the empty string.
                txt = ""
                self._ssntype = self._getTagText(tdtag)
            else:
                txt = self._getTagText(tdtag)
            # The colspan attribute defines how many child headers
            # this section has, so we create that many headers
            # and assign the section name as the value.
            n = int(tdtag["colspan"])
            for j in range(0, n):
                self._hdrs.append(txt)
        # Now we process the second row
        tds = trs[1].find_all("td")
        for i in range(0, len(tds)):
            txt = self._getTagText(tds[i])
            if self._hdrs[i] != "":
                if self._hdrs[i] == "kickoffs" and txt == "avg":
                    # For kickers, the kickoffs section contains 2
                    # children with the text "avg". In each case the
                    # average is for the header in the previous column.
                    # Therefore, we reassign the prefix for this column
                    # to be the value of the previous column.
                    self._hdrs[i] = self._hdrs[i-1]
                # This column has a prefix, therefore, we prepend an
                # underscore to the current value.
                txt = f"_{txt}"
            # Now add the current columns value to the prefix.
            self._hdrs[i] = self._hdrs[i] + txt

    def _incBodyRow(self, trtag : Tag) -> bool:
        mtags = []
        # For each cell
        for tag in trtag.find_all("td"):
            if tag.has_attr("class"):
                # The td tag has a class attribut, which may indicate
                # that the row should not be included.
                classes = tag["class"]
                if any(c in ["border-td", "player-totals"] for c in classes):
                    # The class is either border-td, which indicates that this
                    # is a border row between the data and the player totals
                    # row, or it is player-totals, which indicates that this
                    # is the player totals row. We don't want to include either.
                    mtags.append(tag)
        return len(mtags) == 0

    def _parseBodyRow(self, trtag : Tag) -> list:
        tdtags = trtag.find_all("td")
        data = None
        # If the second column, which is the game data, contains
        # the value "bye", then we don't want to include the
        # row in the output. We indicate that by returning None.
        if self._getTagText(tdtags[1]) != "bye":
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
            "game_date": self._gmdt_parser,
            "opp": self._opp_parser,
            "result": self._result_parser,
            "passing_pct": self._float_parser,
            "passing_avg": self._float_parser,
            "passing_rate": self._float_parser,
            "rushing_avg": self._float_parser,
            "receiving_avg": self._float_parser,
            "overall_fgs_pct": self._float_parser,
            "pat_pct": self._float_parser,
            "kickoffs_ko_avg": self._float_parser,
            "kickoffs_ret_avg": self._float_parser,
            "tackles_sck": self._float_parser,
            "interceptions_avg": self._float_parser,
            "default": self._int_parser
        }
        if header in switch.keys():
            f = switch[header]
        else:
            f = switch["default"]
        return f

    def _opp_parser(self, tdtag : Tag) -> str:
        # The text within the second link tag contains
        # the text we are interested in.
        atags = tdtag.find_all("a")
        return self._getTagText(atags[1], underscores=False, tolower=False)

    def _result_parser(self, tdtag : Tag) -> str:
        # The text within the link tag contains
        # the text we are interested in.
        atag = tdtag.find("a")
        return self._getTagText(atag, underscores=False, tolower=False)

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

    def _float_parser(self, tdtag : Tag) -> float:
        v = self._str_parser(tdtag)
        if v is not None:
            v = float(v)
        return v

    def _gmdt_parser(self, tdtag : Tag) -> float:
        v = self._str_parser(tdtag)
        if v is not None:
            # The game date is just {month}/{day}
            parts = v.split("/")
            # Determine the year based on the season
            # and the month of the game.
            yr = self._season
            if int(parts[0]) < 3:
                # The month is Jan. of Feb. therefore the
                # year is season plus 1.
                yr += 1
            # Create a struct_time for the date. We do so to
            # be consistent with how game dates are stored
            # in the schedule data. Note that there we have
            # the hour and minute in US Eastern time zone,
            # therefore we include the time zone in this date.
            v = time.strptime("{yr}-{mon}-{day} -0500".format(yr=yr, mon=parts[0], day=parts[1]), "%Y-%m-%d %z")
        return v
