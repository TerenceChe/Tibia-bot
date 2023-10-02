from bot.tracker import Tracker

class TestTracker:
    def test_add_player(self):
        tracker = Tracker()
        tracker.add_player("Alice", "Sorcerer")
        assert tracker.players == {"Alice": {"vocation": "Sorcerer", "level": 1, "kills": 0}}

    def test_remove_player(self):
        tracker = Tracker()
        tracker.add_player("Alice", "Sorcerer")
        tracker.remove_player("Alice")
        assert tracker.players == {}

    def test_update_player_level(self):
        tracker = Tracker()
        tracker.add_player("Alice", "Sorcerer")
        tracker.update_player_level("Alice", 10)
        assert tracker.players == {"Alice": {"vocation": "Sorcerer", "level": 10, "kills": 0}}

    def test_update_player_kills(self):
        tracker = Tracker()
        tracker.add_player("Alice", "Sorcerer")
        tracker.update_player_kills("Alice", 1)
        assert tracker.players == {"Alice": {"vocation": "Sorcerer", "level": 1, "kills": 1}}

    def test_get_top_players(self):
        tracker = Tracker()
        tracker.add_player("Alice", "Sorcerer")
        tracker.add_player("Bob", "Knight")
        tracker.update_player_level("Alice", 10)
        tracker.update_player_level("Bob", 20)
        tracker.update_player_kills("Alice", 1)
        tracker.update_player_kills("Bob", 2)
        expected = [("Bob", 20, 2), ("Alice", 10, 1)]
        assert tracker.get_top_players() == expected