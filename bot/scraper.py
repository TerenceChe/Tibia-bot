import requests
from bs4 import BeautifulSoup
from typing import TypeAlias

CharMap: TypeAlias = dict[str, dict[str, str]]
ONLINE_URL = "https://www.noxiousot.com/?subtopic=whoisonline"

def get_page(URL: str) -> requests.Response:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36" }
    page = requests.get(URL, headers=headers)
    return page

def get_char_map() -> CharMap:
    page = get_page(ONLINE_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    char_map = {}

    results = soup.find(id = "whoisonline")
    list_elems = results.find_all("tr", class_="Even")
    list_elems += results.find_all("tr", class_="Odd")

    for char in list_elems:
        name = char.find_all("a")[-1].get_text().strip()
        if len(name.strip()) > 0:
            tds = char.find_all("td")
            level = tds[-2].get_text().strip()
            vocation = tds[-1].get_text().strip()
            char_map[name] = {
                "level" : level, 
                "vocation" : vocation
                }

    return char_map