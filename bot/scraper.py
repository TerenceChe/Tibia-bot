import requests
from bs4 import BeautifulSoup
import time
from typing import TypeAlias, List

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

def get_last_kill_data(last_updated_utc: time.struct_time) -> tuple[List[str], time.struct_time]:
    last_kill_time = last_updated_utc

    res = []
    page = get_page(BASE_URL + LAST_KILL_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_ = "BoxContent")
    trs = results.find_all("tr")
    for tr in trs:
        small_text = tr.find("small")
        if small_text:
            small_text = small_text.getText()
            # DD.MM.YYYY, HH:MM:SS
            kill_time = time.strptime(small_text, "%d.%m.%Y, %H:%M:%S")
            if not kill_time:
                break
            else:
                if last_updated_utc < kill_time:
                    names = [name.text for name in tr.find_all("a")]
                    if len(names) > 1:
                        last_kill_time = last_kill_time if last_kill_time > kill_time else kill_time
                        date = small_text
                        res.append((date, names[0], names[1:]))
    return res, last_kill_time

def get_guild(char_name: str) -> str:
    try:
        page = get_page(BASE_URL + CHARACTER_URL + char_name)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id = "characters")
        results = soup.find_all("a", href=lambda href: href and "?subtopic=guilds&action=show&guild=" in href)[0].get_text()
        return results
    except:
        return ""
