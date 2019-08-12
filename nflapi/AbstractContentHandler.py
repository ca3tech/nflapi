import pandas

class AbstractContentHandler(object):
    """Base ContentHandler for NFL API calls"""

    @property
    def list(self) -> list:
        raise NotImplementedError("abstract base class AbstractContentHandler property list has not been implemented")

    @property
    def dataframe(self) -> pandas.DataFrame:
        raise NotImplementedError("abstract base class AbstractContentHandler property dataframe has not been implemented")
