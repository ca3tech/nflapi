import xml.sax
import pandas
import time
import re

class ScheduleContentHandler(xml.sax.ContentHandler):
    """SAX content handler for parsing a schedule XML file"""

    def __init__(self):
        self._reset()

    @property
    def list(self) -> list:
        return self._data.copy()

    @property
    def dataframe(self) -> pandas.DataFrame:
        return pandas.DataFrame(self.list)

    @property
    def season(self) -> int:
        return self._season

    @property
    def season_type(self) -> int:
        return self._season_type

    @property
    def week(self) -> int:
        return self._week

    def startDocument(self):
        self._reset()

    def startElement(self, name, attrs):
        if name == "gms":
            self._season = int(attrs["y"])
            self._week = int(attrs["w"])
            if attrs["t"] == "R":
                self._season_type = "REG"
        elif name == "g":
            self._data.append(self._parse_game(attrs))

    def _reset(self):
        self._season : int = None
        self._season_type : str = None
        self._week : int = None
        self._data : list = []

    _gmkeymap = {
        "eid": "gsis_id",
        "gsis": "gamekey",
        "d": "day_of_week",
        "t": "start_time",
        "q": "quarter",
        "h": "home_team",
        "hnn": "home_team_name",
        "hs": "home_team_score",
        "v": "away_team",
        "vnn": "away_team_name",
        "vs": "away_team_score",
        "gt": "season_type"
    }

    def _parse_game(self, attrs : dict) -> dict:
        d = {}
        for key in attrs.keys():
            if key in self._gmkeymap.keys():
                val = attrs[key]
                if key in ["hs", "vs"]:
                    if val == "":
                        val = None
                    else:
                        val = int(val)
                d[self._gmkeymap[key]] = val
        d["season"] = self.season
        d["week"] = self.week
        d["finished"] = d["quarter"] in ["F", "FO"]
        
        # Need to parse the start time to a datetime
        d = self._update_start_time(d)

        d = self._set_game_date(d)

        if self._season_type is None:
            self._season_type = d["season_type"]
        return d

    def _update_start_time(self, d : dict) -> dict:
        """
        Unfortunately we have to guess whether the start time is AM or PM
        as the data does not indicate one way or another. I do know that
        the time given is in the US Eastern timezone, i.e. UTC-05.
        """
        rtime = d["start_time"]
        meridiem = "PM"
        hm = [int(_) for _ in rtime.split(":")]
        if hm[0] > 8:
            meridiem = "AM"
        d["start_time"] = time.strptime("{} {} -0500".format(rtime, meridiem), "%I:%M %p %z")
        return d

    def _set_game_date(self, d : dict) -> dict:
        st = d["start_time"]
        m = re.match(r"^(\d{4})(\d{2})(\d{2})", d["gsis_id"])
        d["date"] = time.strptime("{yr}-{mon}-{day} {hr}:{min} -0500".format(yr=m.group(1),
                                                                             mon=m.group(2),
                                                                             day=m.group(3),
                                                                             hr=getattr(st, "tm_hour"),
                                                                             min=getattr(st, "tm_min")),
                                  "%Y-%m-%d %H:%M %z")
        return d
