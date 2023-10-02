from message_format import login_message, level_message, last_kill_message, colour
from table2ascii import table2ascii as t2a, PresetStyle
import time

class TestMessageFormat:
    def test_login_message(self):
        chars = {"Alice": {"level": "10", "vocation": "Sorcerer"}, "Bob": {"level": "20", "vocation": "Knight"}}
        header = ["Name", "Level", "Vocation"]
        body = [["Alice", "10", "Sorcerer"], ["Bob", "20", "Knight"]]

        table = t2a(header=header, body=body, style=PresetStyle.thin_compact)
        expected = f"New player logins:\n```ansi\n{table}```"
        expected = colour(expected)
        
        assert login_message(chars) == expected

    def test_level_message(self):
        chars = {"Alice": {"prev_lvl": "10", "curr_lvl": "20", "vocation": "Sorcerer"}, "Bob": {"prev_lvl": "20", "curr_lvl": "30", "vocation": "Knight"}}
        header = ["Name", "Level", "Vocation"]
        body = [["Alice", "10 -> 20", "Sorcerer"], ["Bob", "20 -> 30", "Knight"]]

        table = t2a(header=header, body=body, style=PresetStyle.thin_compact)
        expected = f"Player level change:\n```ansi\n{table}```"
        expected = colour(expected)
        
        assert level_message(chars) == expected

    # def test_last_kill_message(self):
    #     kill_data = ["Alice killed Bob", "Charlie killed Dave"]
    #     last_updated = time.struct_time((2022, 1, 1, 0, 0, 0, 0, 1, -1))
    #     expected = "Last kills:\n```\nAlice killed Bob\nCharlie killed Dave\n```\nLast updated: 2022-01-01 00:00:00"
    #     assert last_kill_message(kill_data, last_updated) == (expected, last_updated)