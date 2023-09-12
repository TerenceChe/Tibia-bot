import scraper
from typing import TypeAlias

CharMap: TypeAlias = dict[str, dict[str, str]]

def get_logged_in(prev: CharMap, curr: CharMap, min_level: int) -> CharMap:
    new_chars = {}
    for char in curr:
        if (char not in prev and
            int(curr.get(char).get("level")) > min_level):
            new_chars[char] = curr.get(char)
    return(new_chars)


def get_level_diff(prev: CharMap, curr: CharMap, min_level: int) -> CharMap:
    leveled_up = {}
    for char in curr:
        if (char in prev and
            int(curr.get(char).get("level")) != int(prev.get(char).get("level")) and
            int(curr.get(char).get("level")) > min_level):
            vocation = curr.get(char).get("vocation")
            prev_lvl = prev.get(char).get("level")
            curr_lvl = curr.get(char).get("level")
            leveled_up[char] = {
                "vocation" : vocation,
                "prev_lvl" : prev_lvl,
                "curr_lvl" : curr_lvl
            }
    return leveled_up

def get_curr_chars() -> CharMap:
    return scraper.get_char_map()
