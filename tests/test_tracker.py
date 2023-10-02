from unittest.mock import MagicMock, patch
from tracker import get_logged_in, get_level_diff, get_curr_chars, get_last_kill

class TestTracker:
    def test_get_logged_in(self):
        prev = {"Alice": {"level": "10", "vocation": "Sorcerer"}}
        curr = {"Alice": {"level": "20", "vocation": "Sorcerer"}, "Bob": {"level": "30", "vocation": "Knight"}}
        expected = {"Bob": {"level": "30", "vocation": "Knight"}}
        assert get_logged_in(prev, curr, 15) == expected

    def test_get_level_diff(self):
        prev = {"Alice": {"level": "10", "vocation": "Sorcerer"}, "Bob": {"level": "20", "vocation": "Knight"}}
        curr = {"Alice": {"level": "20", "vocation": "Sorcerer"}}
        expected = {"Alice": {"vocation": "Sorcerer", "prev_lvl": "10", "curr_lvl": "20"}}
        assert get_level_diff(prev, curr, 15) == expected

    @patch("tracker.scraper")
    def test_get_curr_chars(self, mock_scraper):
        mock_scraper.get_char_map.return_value = {"Alice": {"level": "10", "vocation": "Sorcerer"}}
        assert get_curr_chars() == {"Alice": {"level": "10", "vocation": "Sorcerer"}}
        mock_scraper.get_char_map.assert_called_once()

    # def test_get_last_kill(self):
    #     scraper = MagicMock()
    #     scraper.get_last_kill_data.return_value = (["Alice killed Bob", "Charlie killed Dave"], (2022, 1, 1, 0, 0, 0, 0, 1, -1))
    #     expected = (["Alice killed Bob", "Charlie killed Dave"], (2022, 1, 1, 0, 0, 0, 0, 1, -1))
    #     assert get_last_kill((2022, 1, 1, 0, 0, 0, 0, 1, -1)) == expected
    #     scraper.get_last_kill_data.assert_called_once_with((2022, 1, 1, 0, 0, 0, 0, 1, -1))