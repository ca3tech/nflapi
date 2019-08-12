from bs4 import Tag
from nflapi.BSTagFilter import BSTagFilter

class PlayerProfileBioFilter(BSTagFilter):
    
    def match(self, tag : Tag) -> bool:
        """Does this tag contain player bio data
        
        Parameters
        ----------
        tag : Tag
            The query tag
        Returns
        -------
        bool
            True if the tag contains player bio data;
            False otherwise
        """
        return tag.name == "div" and tag.has_attr("id") and tag["id"] == "player-bio"
