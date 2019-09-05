from nflapi.GameData import GameData

class MockGameData(GameData):

    def __init__(self, srcpath : str):
        super(MockGameData, self).__init__(False)
        self._qapi_count = 0
        self.srcpath = srcpath

    @property
    def srcpath(self) -> str:
        return self._srcpath

    @srcpath.setter
    def srcpath(self, srcpath : str):
        self._srcpath = srcpath
        with open(srcpath, "rt") as fp:
            self.src = fp.read()

    def _queryAPI(self, schedule : dict) -> str:
        self._qapi_count += 1
        return self.src