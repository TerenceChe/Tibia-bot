import requests
from bs4 import BeautifulSoup
from typing import TypeAlias

CharMap: TypeAlias = dict[str, dict[str, str]]
BASE_URL = "https://www.noxiousot.com"
ONLINE_URL = "/?subtopic=whoisonline"
CHARACTER_URL = "/?subtopic=characters&name="
LAST_KILL_URL = "/?subtopic=killstatistics"

def get_page(URL: str) -> requests.Response:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36" }
    page = requests.get(URL, headers=headers)
    return page

def get_char_map() -> CharMap:
    page = get_page(BASE_URL + ONLINE_URL)
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

def get_last_kill(last_updated_utc):
    page = get_page(BASE_URL, LAST_KILL_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_ = "BoxContent")

    # TODO

def get_guild(char_name: str) -> str:
    try:
        page = get_page(BASE_URL + CHARACTER_URL + char_name)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id = "characters")
        results = soup.find_all("a", href=lambda href: href and "?subtopic=guilds&action=show&guild=" in href)[0].get_text()
        return results
    except:
        return ""

if __name__ == "__main__":
    print(get_guild("awelkf"))
