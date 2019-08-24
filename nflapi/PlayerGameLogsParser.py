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
        self._parseHeader(tag.find("thead"))
        tbtag = tag.find("tbody")
        data = []
        for trtag in tbtag.find_all("tr"):
            if self._incBodyRow(trtag):
                rl = self._parseBodyRow(trtag)
                if rl is not None:
                    d = dict(zip(self._headers, rl))
                    d["season"] = self._season
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
        trs : list = thtag.find_all("tr")
        tds : list = trs[0].find_all("td")
        for i in range(0, len(tds)):
            tdtag = tds[i]
            if i == 0:
                txt = ""
                self._ssntype = self._getTagText(tdtag)
            else:
                txt = self._getTagText(tdtag)
            n = int(tdtag["colspan"])
            for j in range(0, n):
                self._hdrs.append(txt)
        tds = trs[1].find_all("td")
        for i in range(0, len(tds)):
            txt = self._getTagText(tds[i])
            if self._hdrs[i] != "":
                txt = f"_{txt}"
            self._hdrs[i] = self._hdrs[i] + txt

    def _incBodyRow(self, trtag : Tag) -> bool:
        mtags = []
        for tag in trtag.find_all("td"):
            if tag.has_attr("class"):
                classes = tag["class"]
                if any(c in ["border-td", "player-totals"] for c in classes):
                    mtags.append(tag)
        return len(mtags) == 0

    def _parseBodyRow(self, trtag : Tag) -> list:
        tdtags = trtag.find_all("td")
        data = None
        if self._getTagText(tdtags[1]) != "bye":
            data = []
            for i in range(0, len(tdtags)):
                pfun = self._getBodyColParser(self._headers[i])
                data.append(pfun(tdtags[i]))
        return data

    def _getTagText(self, tag : Tag, underscores : bool = True, tolower : bool = True) -> str:
        txt = tag.get_text()
        txt = re.sub(r"\s+$", "", txt)
        txt = re.sub(r"^\s+", "", txt)
        txt = re.sub(r"\s{2,}", " ", txt)
        if underscores:
            txt = re.sub(" ", "_", txt)
        if tolower:
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
            "default": self._int_parser
        }
        if header in switch.keys():
            f = switch[header]
        else:
            f = switch["default"]
        return f

    def _opp_parser(self, tdtag : Tag) -> str:
        atags = tdtag.find_all("a")
        return self._getTagText(atags[1], underscores=False, tolower=False)

    def _result_parser(self, tdtag : Tag) -> str:
        atag = tdtag.find("a")
        return self._getTagText(atag, underscores=False, tolower=False)

    def _str_parser(self, tdtag : Tag) -> str:
        v : str = self._getTagText(tdtag, underscores=False, tolower=False)
        if v in ["--", ""]:
            v = None
        return v

    def _int_parser(self, tdtag : Tag) -> int:
        v = self._str_parser(tdtag)
        if v is not None:
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
            parts = v.split("/")
            yr = self._season
            if int(parts[0]) < 3:
                yr += 1
            v = time.strptime("{yr}-{mon}-{day} -0500".format(yr=yr, mon=parts[0], day=parts[1]), "%Y-%m-%d %z")
        return v
