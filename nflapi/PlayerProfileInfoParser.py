from bs4 import Tag
import re

class PlayerProfileInfoParser(object):
    
    def parse(self, tag : Tag) -> dict:
        d = {}
        for ptag in tag.find_all("p"):
            for stag in ptag.find_all("strong"):
                key = re.sub(r" {2,}", " ", stag.string.lower())
                key = key.replace(" ", "_")
                value = stag.next_sibling.string
                value = re.sub(r"\s+$", "", value)
                value = re.sub(r"^[:\s]+", "", value)
                value = re.sub(r" {2,}", " ", value)
                value = re.sub(r"\s+\,", ",", value)
                if key in ("age", "weight"):
                    value = int(value)
                d[key] = value
        return d