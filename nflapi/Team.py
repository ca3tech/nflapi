
class Team(object):

    @staticmethod
    def teams() -> list:
        """Get a list of team abbreviations used by the NFL
        
        Returns
        -------
        list of str
        """
        return list(__TEAM__)

    @staticmethod
    def is_team(value : str) -> bool:
        """Test whether a string is a valid team abbreviation

        Returns
        -------
        bool
            True of value is a valid team abbreviation,
            False otherwise
        """
        return value in Team.teams()

    def __init__(self, team : str):
        """constructor

        Parameters
        ----------
        team : str
            The NFL team abbreviation this team is for
        """
        self._team = team

    @property
    def team(self) -> str:
        return self._team

    @property
    def name(self) -> str:
        return self._get("name")

    @property
    def fullname(self) -> str:
        fname = self._get("fullname")
        if fname is None:
            fname = f"{self.city} {self.name}"
        return fname

    @property
    def city(self) -> str:
        return self._get("city")

    @property
    def state(self) -> str:
        return self._get("state")

    @property
    def latitude(self) -> float:
        return self._get("lat")

    @property
    def longitude(self) -> float:
        return self._get("lon")

    @property
    def is_active(self) -> bool:
        return self._get("active")

    def _get(self, key : str) -> any:
        value = None
        if self.team in __TEAM__ and key in __TEAM__[self.team]:
            value = __TEAM__[self.team][key]
        return value

    def __str__(self) -> str:
        return self.team

    def __repr__(self) -> str:
        return f"Team({self.team})"

    @property
    def __dict__(self) -> dict:
        return {
            "team": self.team,
            "name": self.name,
            "fullname": self.fullname,
            "city": self.city,
            "state": self.state,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "is_active": self.is_active
        }

    # Make objects usable in collections

    def __hash__(self) -> int:
        return hash(self.team)

    def __eq__(self, other : any) -> bool:
        return str(self) == str(other)

    def __lt__(self, other : any) -> bool:
        return str(self) < str(other)

    def __le__(self, other : any) -> bool:
        return str(self) <= str(other)

    def __gt__(self, other : any) -> bool:
        return str(self) > str(other)

    def __ge__(self, other : any) -> bool:
        return str(self) >= str(other)

__TEAM__ = {
    "ARI": {"name": "Cardinals", "city": "Phoenix", "fullname": "Arizona Cardinals", "state": "Arizona", "lat": 33.5275, "lon": -112.2625, "active": True},
    "ATL": {"name": "Falcons", "city": "Atlanta", "state": "Georgia", "lat": 33.755, "lon": -84.401, "active": True},
    "BAL": {"name": "Ravens", "city": "Baltimore", "state": "Maryland", "lat": 39.278056, "lon": -76.622778, "active": True},
    "BUF": {"name": "Bills", "city": "Buffalo", "state": "New Yord", "lat": 42.774, "lon": -78.787, "active": True},
    "CAR": {"name": "Panthers", "fullname": "Carolina Panthers", "city": "Charlotte", "state": "North Carolina", "lat": 35.225833, "lon": -80.852778, "active": True},
    "CHI": {"name": "Bears", "city": "Chicago", "state": "Illinois", "lat": 41.8623, "lon": -87.6167, "active": True},
    "CIN": {"name": "Bengals", "city": "Cincinnati", "state": "Ohio", "lat": 39.095, "lon": -84.516, "active": True},
    "CLE": {"name": "Browns", "city": "Cleveland", "state": "Ohio", "lat": 41.506111, "lon": -81.699444, "active": True},
    "DAL": {"name": "Cowboys", "city": "Dallas", "state": "Texas", "lat": 32.747778, "lon": -97.092778, "active": True},
    "DEN": {"name": "Broncos", "city": "Denver", "state": "Colorado", "lat": 39.743889, "lon": -105.02, "active": True},
    "DET": {"name": "Lions", "city": "Detroit", "state": "Michigan", "lat": 42.34, "lon": -83.045556, "active": True},
    "GB": {"name": "Packers", "city": "Green Bay", "state": "Wisconsin", "lat": 44.501389, "lon": -88.062222, "active": True},
    "HOU": {"name": "Texans", "city": "Houston", "state": "Texas", "lat": 29.684722, "lon": -95.410833, "active": True},
    "IND": {"name": "Colts", "city": "Indianapolis", "state": "Indiana", "lat": 39.760056, "lon": -86.163806, "active": True},
    "JAX": {"name": "Jaguars", "city": "Jacksonville", "state": "Florida", "lat": 30.323889, "lon": -81.6375, "active": True},
    "KC": {"name": "Chiefs", "city": "Kansas City", "state": "Missouri", "lat": 39.048889, "lon": -94.483889, "active": True},
    "LAC": {"name": "Chargers", "city": "Los Angeles", "state": "California", "lat": 33.864, "lon": -118.261, "active": True},
    "LA": {"name": "Rams", "city": "Los Angeles", "state": "California", "lat": 34.014167, "lon": -118.287778, "active": True},
    "MIA": {"name": "Dolphins", "city": "Miami", "state": "Florida", "lat": 25.958056, "lon": -80.238889, "active": True},
    "MIN": {"name": "Vikings", "fullname": "Minnesota Vikings", "city": "Minneapolis", "state": "Minnesota", "lat": 44.974, "lon": -93.258, "active": True},
    "NE": {"name": "Patriots", "fullname": "New England Patriots", "city": "Foxborough", "state": "Massachusetts", "lat": 42.09094432, "lon": -71.264344, "active": True},
    "NO": {"name": "Saints", "city": "New Orleans", "state": "Louisiana", "lat": 29.950833, "lon": -90.081111, "active": True},
    "NYG": {"name": "Giants", "city": "New York", "state": "New York", "lat": 40.813528, "lon": -74.074361, "active": True},
    "NYJ": {"name": "Jets", "city": "New York", "state": "New York", "lat": 40.813528, "lon": -74.074361, "active": True},
    "OAK": {"name": "Raiders", "city": "Oakland", "state": "California", "lat": 37.751667, "lon": -122.200556, "active": True},
    "PHI": {"name": "Eagles", "city": "Philadelphia", "state": "Pennsylvania", "lat": 39.900833, "lon": -75.1675, "active": True},
    "PIT": {"name": "Steelers", "city": "Pittsburgh", "state": "Pennsylvania", "lat": 40.446667, "lon": -80.015833, "active": True},
    "SEA": {"name": "Seahawks", "city": "Seattle", "state": "Washington", "lat": 47.5952, "lon": -122.3316, "active": True},
    "SF": {"name": "49ers", "city": "San Francisco", "state": "California", "lat": 37.403, "lon": -121.97, "active": True},
    "TB": {"name": "Buccaneers", "fullname": "Tampa Bay Buccaneers", "city": "Tampa", "state": "Florida", "lat": 27.975833, "lon": -82.503333, "active": True},
    "TEN": {"name": "Titans", "fullname": "Tennessee Titans", "city": "Nashville", "state": "Tennessee", "lat": 36.166389, "lon": -86.771389, "active": True},
    "WAS": {"name": "Redskins", "fullname": "Washington Redskins", "city": "Landover", "state": "Maryland", "lat": 38.907778, "lon": -76.864444, "active": True},
    "SD": {"name": "Chargers", "city": "San Diego", "state": "California", "lat": 32.783056, "lon": -117.119444, "active": False},
    "STL": {"name": "Rams", "city": "St. Louis", "state": "Missouri", "lat": 38.631035, "lon": -90.190918, "active": False}
}
