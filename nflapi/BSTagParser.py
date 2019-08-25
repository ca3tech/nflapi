from abc import ABC, abstractmethod
from bs4 import Tag
from typing import List

class BSTagParser(ABC):

    @abstractmethod
    def parse(self, tag : Tag) -> List[dict]:
        """Implement this in your subclass
        
        Parse the content of interest from the provided
        tag and reaturn it as a list of dicts

        Parameters
        ----------
        tag : Tag
            The subject tag from BeautifulSoup
        """
        pass