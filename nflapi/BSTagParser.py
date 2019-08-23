from abc import ABC, abstractmethod
from bs4 import Tag
from typing import List

class BSTagParser(ABC):

    @abstractmethod
    def parse(self, tag : Tag) -> List[dict]:
        pass