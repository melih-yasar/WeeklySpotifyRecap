import unittest

import os
import sys
from pathlib import Path


SRC = Path(__file__).resolve().parent / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

TEST_ENV = {
    "LASTFM_API_KEY": "test-lastfm-key",
    "LASTFM_USERNAME": "test-user",
    "SPOTIFY_CLIENT_ID": "test-client-id",
    "SPOTIFY_CLIENT_SECRET": "test-client-secret",
    "SPOTIFY_REFRESH_TOKEN": "test-refresh-token",
    "SPOTIFY_PLAYLIST_ID": "test-playlist-id",
    "SPOTIFY_PLAYLIST_NAME": "Weekly Spotify Recap",
    "GMAIL_ADDRESS": "sender@example.com",
    "GMAIL_APP_PASSWORD": "test-app-password",
    "RECIPIENT_EMAIL": "recipient@example.com",
    "PLAYLIST_URL": "https://open.spotify.com/playlist/test",
    "PLAYLIST_COVER_PATH": "assets/playlist-cover.jpg",
}

for key, value in TEST_ENV.items():
    os.environ[key] = value
from weekly_spotify_recap import music_helpers


class MusicHelpersTests(unittest.TestCase):
    def test_normalize_name_removes_case_and_symbols(self):
        self.assertEqual(music_helpers.normalize_name("AC/DC - Live!"), "acdclive")

    def test_exact_name_match_matches_normalized_values(self):
        self.assertTrue(music_helpers.exact_name_match("Song Title!", "song title"))

    def test_estimate_listening_hours_uses_average_song_length(self):
        self.assertEqual(music_helpers.estimate_listening_hours(60), 3.5)

    def test_relaxed_album_match_handles_roman_numerals(self):
        self.assertTrue(music_helpers.relaxed_album_match("Chapter IV", "Chapter 4"))

    def test_find_album_for_track_returns_unknown_for_missing_track(self):
        summary = {"raw_tracks": [{"artist": "A", "title": "T", "album": "Album"}]}
        self.assertEqual(
            music_helpers.find_album_for_track(summary, "Missing", "Track"),
            "Unknown Album",
        )


if __name__ == "__main__":
    unittest.main()


