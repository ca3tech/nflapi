from bs4 import Tag
import re
from typing import List
from nflapi.BSTagParser import BSTagParser

class PlayerProfileInfoParser(BSTagParser):
    
    def parse(self, tag : Tag) -> List[dict]:
        """Parse a profile info tag for player information
        
        Parameters
        ----------
        tag : Tag
            The player info div tag from BeautifulSoup
        
        Returns
        -------
        list of dict
            A single element list with the player information
            as the sole record
        """
        d = {}
        # Each item is contained in a p tag
        for ptag in tag.find_all("p"):
            pntag = ptag.find_all(lambda qtag: qtag.name == "span" and
                                               qtag.has_attr("class") and
                                               qtag["class"] == ["player-number"])
            if len(pntag) > 0:
                words = pntag[0].string.split(" ")
                num = words[0].strip("#")
                if num != "":
                    d["number"] = int(num)
                d["position"] = words[1]
            # The key for the record is contained in a strong tag
            for stag in ptag.find_all("strong"):
                # Extract the tag text
                # Convert it to lower case
                # Replace multiple spaces with a single space
                key = re.sub(r" {2,}", " ", stag.string.lower())
                # Convert spaces to underscores
                key = key.replace(" ", "_")
                # The value is stored as the text of the next tag
                value = stag.next_sibling.string
                # Strip trailing whitespace
                value = re.sub(r"\s+$", "", value)
                # Strip preceeding whitespace and colons
                value = re.sub(r"^[:\s]+", "", value)
                # Replace multiple spaces with a single space
                value = re.sub(r" {2,}", " ", value)
                # Remove any whitespace preceeding a comma
                value = re.sub(r"\s+\,", ",", value)
                if key in ("age", "weight"):
                    value = int(value)
                d[key] = value
        return [d]