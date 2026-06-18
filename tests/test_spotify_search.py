import unittest
from unittest.mock import patch

import os
import sys
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"

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
from weekly_spotify_recap import spotify_search


class SpotifySearchTests(unittest.TestCase):
    def test_find_spotify_track_returns_matching_track(self):
        data = {
            "tracks": {
                "items": [{
                    "name": "Song A",
                    "uri": "spotify:track:1",
                    "external_urls": {"spotify": "https://track"},
                    "artists": [{"name": "Artist A"}],
                    "album": {"name": "Album A", "images": [{"url": "https://cover"}]},
                }]
            }
        }

        with patch("weekly_spotify_recap.spotify_search.spotify_search", return_value=data):
            track = spotify_search.find_spotify_track("artist a", "song a")

        self.assertEqual(track["uri"], "spotify:track:1")
        self.assertEqual(track["album_cover_url"], "https://cover")

    def test_find_spotify_track_returns_none_without_match(self):
        data = {"tracks": {"items": [{"name": "Other", "artists": []}]}}

        with patch("weekly_spotify_recap.spotify_search.spotify_search", return_value=data):
            track = spotify_search.find_spotify_track("Artist A", "Song A")

        self.assertIsNone(track)


if __name__ == "__main__":
    unittest.main()


