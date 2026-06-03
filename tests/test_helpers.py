import unittest

import test_support  # noqa: F401
from weekly_spotify_recap import helpers


class HelpersTests(unittest.TestCase):
    def test_normalize_name_removes_case_and_symbols(self):
        self.assertEqual(helpers.normalize_name("AC/DC - Live!"), "acdclive")

    def test_exact_name_match_matches_normalized_values(self):
        self.assertTrue(helpers.exact_name_match("Song Title!", "song title"))

    def test_estimate_listening_hours_uses_average_song_length(self):
        self.assertEqual(helpers.estimate_listening_hours(60), 3.5)

    def test_relaxed_album_match_handles_roman_numerals(self):
        self.assertTrue(helpers.relaxed_album_match("Chapter IV", "Chapter 4"))

    def test_find_album_for_track_returns_unknown_for_missing_track(self):
        summary = {"raw_tracks": [{"artist": "A", "title": "T", "album": "Album"}]}
        self.assertEqual(
            helpers.find_album_for_track(summary, "Missing", "Track"),
            "Unknown Album",
        )


if __name__ == "__main__":
    unittest.main()
