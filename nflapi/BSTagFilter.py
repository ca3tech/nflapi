from bs4 import Tag
from abc import ABC, abstractmethod

class BSTagFilter(ABC):

    @abstractmethod
    def match(self, tag : Tag) -> bool:
        """Implement this in your subclass
        
        Does the given tag contain data that we care about?

        Parameters
        ----------
        tag : Tag
            The subject tag from BeautifulSoup
        """
        pass
