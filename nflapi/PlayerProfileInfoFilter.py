from bs4 import Tag
from nflapi.BSTagFilter import BSTagFilter

class PlayerProfileInfoFilter(BSTagFilter):
    
    def match(self, tag : Tag) -> bool:
        """Does this tag contain player bio info data
        
        Parameters
        ----------
        tag : Tag
            The query tag
        Returns
        -------
        bool
            True if the tag contains player bio info data;
            False otherwise
        """
        return tag.name == "div" and tag.has_attr("class") and tag["class"] == ["player-info"]
