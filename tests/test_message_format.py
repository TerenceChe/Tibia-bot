from bot.message_format import login_message, level_message, last_kill_message
import time

class TestMessageFormat:
    def test_login_message(self):
        chars = {"Alice": {"level": "10", "vocation": "Sorcerer"}, "Bob": {"level": "20", "vocation": "Knight"}}
        expected = "New player logins:\n```ansi\n+-------+-------+-----------+\n| Name  | Level | Vocation  |\n+-------+-------+-----------+\n| Alice | 10    | Sorcerer |\n| Bob   | 20    | Knight    |\n+-------+-------+-----------+\n```"
        assert login_message(chars) == expected

    def test_level_message(self):
        chars = {"Alice": {"prev_lvl": "10", "curr_lvl": "20", "vocation": "Sorcerer"}, "Bob": {"prev_lvl": "20", "curr_lvl": "30", "vocation": "Knight"}}
        expected = "Player level change:\n```ansi\n+-------+-------+-----------+\n| Name  | Level | Vocation  |\n+-------+-------+-----------+\n| Alice | 10 -> 20 | Sorcerer |\n| Bob   | 20 -> 30 | Knight    |\n+-------+-------+-----------+\n```"
        assert level_message(chars) == expected

    def test_last_kill_message(self):
        kill_data = ["Alice killed Bob", "Charlie killed Dave"]
        last_updated = time.struct_time((2022, 1, 1, 0, 0, 0, 0, 1, -1))
        expected = "Last kills:\n```\nAlice killed Bob\nCharlie killed Dave\n```\nLast updated: 2022-01-01 00:00:00"
        assert last_kill_message(kill_data, last_updated) == (expected, last_updated)