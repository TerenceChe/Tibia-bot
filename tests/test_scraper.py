from bot.scraper import get_page, get_char_map

class TestScraper:
    def test_get_page(self):
        page = get_page("https://www.noxiousot.com/?subtopic=whoisonline")
        assert page.status_code == 200

    def test_get_char_map(self):
        char_map = get_char_map()
        assert isinstance(char_map, dict)
        assert len(char_map) > 0
        for name, char_info in char_map.items():
            assert isinstance(name, str)
            assert isinstance(char_info, dict)
            assert "level" in char_info
            assert "vocation" in char_info