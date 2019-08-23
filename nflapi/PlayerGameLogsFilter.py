from bs4 import Tag
from nflapi.BSTagFilter import BSTagFilter

class PlayerGameLogsFilter(BSTagFilter):

    def match(self, tag : Tag) -> bool:
        """Does this tag contain game log data
        
        Parameters
        ----------
        tag : Tag
            The query tag
        Returns
        -------
        bool
            True if the tag contains game log data;
            False otherwise
        """
        return (tag.name == "table"
                and tag.has_attr("class") and tag["class"] == ["data-table1"]
                and tag.has_attr("summary") and tag["summary"].startswith("Game Logs"))