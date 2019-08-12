from bs4 import Tag
from abc import ABC, abstractmethod

class BSTagFilter(ABC):

    @abstractmethod
    def match(self, tag : Tag) -> bool:
        pass
